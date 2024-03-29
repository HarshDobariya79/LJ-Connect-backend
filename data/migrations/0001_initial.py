# Generated by Django 4.1.7 on 2023-06-18 11:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='dd/mm/yyyy', verbose_name='Date')),
                ('mode', models.CharField(choices=[('R', 'Regular'), ('PRX', 'proxy')], default='R', max_length=5, verbose_name='Mode')),
                ('present', models.BooleanField(help_text='If student is present or not.', verbose_name='Present')),
            ],
            options={
                'verbose_name': 'Attendance',
                'verbose_name_plural': 'Attendances',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='Batch Name')),
            ],
            options={
                'verbose_name': 'Batch',
                'verbose_name_plural': 'Batches',
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('branch_code', models.CharField(max_length=15, primary_key=True, serialize=False, verbose_name='Branch Code')),
                ('branch_short_name', models.CharField(help_text='e.g. CSE', max_length=10, verbose_name='Branch Name')),
                ('branch_full_name', models.CharField(help_text='e.g. Computer Science and Engineering', max_length=50, verbose_name='Branch Full Name')),
                ('available', models.BooleanField(default=True, help_text='If branch is currently available to enrollment.', verbose_name='Available')),
            ],
            options={
                'verbose_name': 'Branch',
                'verbose_name_plural': 'Branches',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(help_text='e.g. 2022-23', max_length=7, verbose_name='Year')),
                ('semester', models.PositiveSmallIntegerField(help_text='e.g. 1', verbose_name='Semester')),
                ('name', models.CharField(help_text='e.g. CE_IT_2', max_length=20, verbose_name='Department Name')),
                ('batch', models.ManyToManyField(to='data.batch', verbose_name='Batch')),
                ('branch', models.ManyToManyField(to='data.branch', verbose_name='Branch')),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='GroupProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('definition', models.TextField(verbose_name='Project Definition')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Create Timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Update Timestamp')),
            ],
            options={
                'verbose_name': 'Group Project',
                'verbose_name_plural': 'Group Projects',
            },
        ),
        migrations.CreateModel(
            name='IndividualProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('definition', models.TextField(verbose_name='Project Definition')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Create Timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Update Timestamp')),
            ],
            options={
                'verbose_name': 'Individual Project',
                'verbose_name_plural': 'Individual Projects',
            },
        ),
        migrations.CreateModel(
            name='MOOCCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=100, verbose_name='Course')),
                ('platform', models.CharField(help_text='e.g. Coursera', max_length=30, verbose_name='Platform')),
                ('university', models.CharField(max_length=60, verbose_name='University')),
            ],
            options={
                'verbose_name': 'MOOC Course',
                'verbose_name_plural': 'MOOC Courses',
            },
        ),
        migrations.CreateModel(
            name='MOOCResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.FloatField(blank=True, null=True, verbose_name='Percentage')),
                ('certificate', models.URLField(blank=True, null=True, verbose_name='Certificate')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.mooccourse', verbose_name='MOOC Course')),
            ],
            options={
                'verbose_name': 'MOOC Result',
                'verbose_name_plural': 'MOOC Results',
            },
        ),
        migrations.CreateModel(
            name='RemedialTestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theory', models.FloatField(blank=True, null=True, verbose_name='Theory')),
                ('individual_project', models.FloatField(blank=True, null=True, verbose_name='Individual Project')),
                ('group_project', models.FloatField(blank=True, null=True, verbose_name='Group project')),
                ('ipe', models.FloatField(blank=True, null=True, verbose_name='IPE')),
                ('other', models.FloatField(blank=True, null=True, verbose_name='other')),
            ],
            options={
                'verbose_name': 'Remedial Test Result',
                'verbose_name_plural': 'Remedial Test Results',
            },
        ),
        migrations.CreateModel(
            name='StaffDetail',
            fields=[
                ('email', models.EmailField(help_text='e.g. firstname.lastname@ljku.edu.in', max_length=100, primary_key=True, serialize=False, verbose_name='Email')),
                ('first_name', models.CharField(max_length=20, verbose_name='First Name')),
                ('middle_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Middle Name')),
                ('last_name', models.CharField(max_length=20, verbose_name='Last Name')),
                ('short_name', models.CharField(help_text='e.g. DKT', max_length=5, verbose_name='Short Name')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, verbose_name='Gender')),
                ('birth_date', models.DateField(help_text='dd/mm/yyyy', verbose_name='Birth Date')),
                ('mobile_number', models.CharField(help_text='e.g. +911234567890', max_length=15, validators=[django.core.validators.RegexValidator(message='Mobile number must be in international format with no spaces or special characters.', regex='^\\+?\\d{6,15}$')], verbose_name='Mobile Number')),
                ('category', models.CharField(choices=[('T', 'Teaching'), ('NT', 'Non-Teaching')], max_length=2, verbose_name='Category')),
                ('active', models.BooleanField(default=True, help_text='Is the staff actively doing his/her job?', verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Staff Detail',
                'verbose_name_plural': 'Staff Details',
            },
        ),
        migrations.CreateModel(
            name='StudentDetail',
            fields=[
                ('enrolment_no', models.CharField(max_length=16, primary_key=True, serialize=False, verbose_name='Enrolmentment No')),
                ('email', models.EmailField(help_text='e.g. enrolment_number@ljku.edu.in', max_length=30, unique=True, verbose_name='Email')),
                ('first_name', models.CharField(max_length=20, verbose_name='First Name')),
                ('middle_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Middle Name')),
                ('last_name', models.CharField(max_length=20, verbose_name='Last Name')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, verbose_name='Gender')),
                ('birth_date', models.DateField(help_text='dd/mm/yyyy', verbose_name='Birth Date')),
                ('mobile_number', models.CharField(help_text='e.g. +1234567890', max_length=15, validators=[django.core.validators.RegexValidator(message='Mobile number must be in international format with no spaces or special characters.', regex='^\\+?\\d{6,15}$')], verbose_name='Mobile Number')),
                ('branch', models.ForeignKey(help_text='Branch details where student is enrolled.', on_delete=django.db.models.deletion.CASCADE, to='data.branch', verbose_name='Branch')),
            ],
            options={
                'verbose_name': 'Student Detail',
                'verbose_name_plural': 'Student Details',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('subject_code', models.CharField(max_length=15, primary_key=True, serialize=False, verbose_name='Subject Code')),
                ('subject_short_name', models.CharField(help_text='e.g. FCSP-I', max_length=10, verbose_name='Subject Short Name')),
                ('subject_full_name', models.CharField(help_text='Fundamentals of Computer Science using Python-I', max_length=50, verbose_name='Subject Full Name')),
                ('total_credit', models.PositiveSmallIntegerField(help_text='Total credit of the subject.', verbose_name='Total Credit')),
                ('theory_credit', models.PositiveSmallIntegerField(help_text='Theory credit of the subject.', verbose_name='Theory Credit')),
                ('tutorial_credit', models.PositiveSmallIntegerField(blank=True, help_text='Tutorial credit of the subject.', null=True, verbose_name='Tutorial Credit')),
                ('practical_credit', models.PositiveSmallIntegerField(blank=True, help_text='Practical credit of the subject.', null=True, verbose_name='Practical Credit')),
            ],
            options={
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
            },
        ),
        migrations.CreateModel(
            name='Weightage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teaching_type', models.CharField(choices=[('T', 'Theory'), ('P', 'Practical'), ('TU', 'Tutorial')], max_length=2, verbose_name='Teaching Type')),
                ('category', models.CharField(choices=[('MCQ', 'MCQ'), ('THEORY_DESC', 'Theory Descriptive'), ('FORMULA_DERIVATION', 'Formulas and Derivation'), ('NUMERICAL', 'Numerical'), ('INDIVIDUAL_PROJ', 'Individual Project'), ('IPE', 'Internal Practical Evaluation (IPE)'), ('GROUP_PROJ', 'Group Project'), ('VIVA', 'Viva'), ('SEMINAR', 'Seminar')], max_length=25, verbose_name='Category')),
                ('percentage_weightage', models.PositiveSmallIntegerField(help_text='Percentage weightage distribution.', verbose_name='Percentage Weightage')),
                ('marks_weightage', models.PositiveSmallIntegerField(help_text='Marks weightage distribution.', verbose_name='Marks Weightage')),
            ],
            options={
                'verbose_name': 'Subject Weightage',
                'verbose_name_plural': 'Subject Weightages',
            },
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('T1', models.FloatField(blank=True, help_text='Test 1 Result', null=True, verbose_name='T1')),
                ('T2', models.FloatField(blank=True, help_text='Test 2 Result', null=True, verbose_name='T2')),
                ('T3', models.FloatField(blank=True, help_text='Test 3 Result', null=True, verbose_name='T3')),
                ('T4', models.FloatField(blank=True, help_text='Test 4 Result', null=True, verbose_name='T4')),
                ('T1_file', models.FileField(blank=True, help_text='Test 1 Scanned Copy', null=True, upload_to='test_files/', verbose_name='T1 Files')),
                ('T2_file', models.FileField(blank=True, help_text='Test 2 Scanned Copy', null=True, upload_to='test_files/', verbose_name='T2 Files')),
                ('T3_file', models.FileField(blank=True, help_text='Test 3 Scanned Copy', null=True, upload_to='test_files/', verbose_name='T3 Files')),
                ('T4_file', models.FileField(blank=True, help_text='Test 4 Scanned Copy', null=True, upload_to='test_files/', verbose_name='T4 Files')),
                ('individual_project', models.FloatField(blank=True, null=True, verbose_name='Individual Project')),
                ('group_project', models.FloatField(blank=True, null=True, verbose_name='Group Project')),
                ('ipe', models.FloatField(blank=True, help_text='IPE Marks', null=True, verbose_name='IPE')),
                ('other', models.FloatField(blank=True, null=True, verbose_name='Other')),
                ('bonus', models.FloatField(blank=True, help_text='HOD Bonus, Attendance Bonus etc.', null=True, verbose_name='Bonus')),
                ('remedial_result', models.ManyToManyField(to='data.remedialtestresult', verbose_name='Remedial Result')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.subject', verbose_name='Subject')),
            ],
            options={
                'verbose_name': 'Test Result',
                'verbose_name_plural': 'Test Results',
            },
        ),
        migrations.AddField(
            model_name='subject',
            name='Weightage',
            field=models.ManyToManyField(help_text='Weightage distribution of the subject', to='data.weightage', verbose_name='Weightage'),
        ),
        migrations.CreateModel(
            name='StudyResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Resource Name')),
                ('resource_type', models.CharField(max_length=50, verbose_name='Resource Type')),
                ('upload_date', models.DateField(auto_now=True, help_text='dd/mm/yyyy', verbose_name='Upload Date')),
                ('file', models.FileField(upload_to='study_resources/', verbose_name='Study Resource File')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.subject', verbose_name='Subject')),
            ],
            options={
                'verbose_name': 'Study Resource',
                'verbose_name_plural': 'Study Resources',
            },
        ),
        migrations.CreateModel(
            name='StudentSemesterRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_no', models.PositiveSmallIntegerField(verbose_name='Roll No')),
                ('MOOC_courses', models.ManyToManyField(to='data.moocresult', verbose_name='MOOC Courses')),
                ('attendance', models.ManyToManyField(to='data.attendance', verbose_name='Attendance')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.department', verbose_name='Department')),
                ('group_project', models.ManyToManyField(to='data.groupproject', verbose_name='Group Project')),
                ('individual_project', models.ManyToManyField(to='data.individualproject', verbose_name='Individual Project')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.studentdetail', verbose_name='Student Details')),
                ('test_result', models.ManyToManyField(to='data.testresult', verbose_name='Test Result')),
            ],
            options={
                'verbose_name': 'Student Semester Record',
                'verbose_name_plural': 'Student Semester Records',
            },
        ),
        migrations.AddField(
            model_name='individualproject',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.subject', verbose_name='Subject'),
        ),
        migrations.AddField(
            model_name='groupproject',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.subject', verbose_name='Subject'),
        ),
        migrations.CreateModel(
            name='FacultyAllocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty', models.ForeignKey(help_text='Faculty details', on_delete=django.db.models.deletion.CASCADE, to='data.staffdetail', verbose_name='Faculty')),
                ('subject', models.ForeignKey(help_text='Subject details', on_delete=django.db.models.deletion.CASCADE, to='data.subject', verbose_name='Subject')),
            ],
            options={
                'verbose_name': 'Faculty Allocation',
                'verbose_name_plural': 'Faculty Allocation',
            },
        ),
        migrations.AddField(
            model_name='department',
            name='hod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.staffdetail', verbose_name='Head of Department'),
        ),
        migrations.AddField(
            model_name='department',
            name='study_resources',
            field=models.ManyToManyField(to='data.studyresource', verbose_name='Study Resources'),
        ),
        migrations.AddField(
            model_name='batch',
            name='faculty',
            field=models.ManyToManyField(help_text='Faculty allocated to batch', to='data.facultyallocation', verbose_name='Faculty'),
        ),
        migrations.AddField(
            model_name='batch',
            name='student',
            field=models.ManyToManyField(help_text='Student allocated to batch', to='data.studentdetail', verbose_name='Student'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.subject', verbose_name='Subject'),
        ),
    ]
