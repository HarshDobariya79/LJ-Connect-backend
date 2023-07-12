from django.contrib import admin  
from .models import StaffDetail, Weightage, Subject, Branch, StudentDetail, FacultyAllocation, Batch, StudyResource, Department, Attendance, RemedialTestResult, TestResult, MOOCCourse, MOOCResult, IndividualProject, GroupProject, StudentSemesterRecord


class StaffDetailAdmin(admin.ModelAdmin):
    search_fields = ['email', 'short_name']

class WeightageAdmin(admin.ModelAdmin):
    search_fields = ['subject__subject_short_name', 'teaching_type', 'category']

class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['subject_code', 'subject_short_name']

class BranchAdmin(admin.ModelAdmin):
    search_fields = ['branch_code', 'branch_short_name']

class StudentDetailAdmin(admin.ModelAdmin):
    search_fields = ['email', 'enrolment_no']

class FacultyAllocationAdmin(admin.ModelAdmin):
    search_fields = ['faculty__email', 'subject__subject_code', 'subject__subject_short_name']

class BatchAdmin(admin.ModelAdmin):
    search_fields = ['name']

class StudyResourceAdmin(admin.ModelAdmin):
    search_fields = ['name']

class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ['name', 'year']

class AttendanceAdmin(admin.ModelAdmin):
    search_fields = ['studentsemesterrecord__student__enrolment_no', 'studentsemesterrecord__student__email','date']

class RemedialTestResultAdmin(admin.ModelAdmin):
    search_fields = ['testresult__subject__subject_code', 'testresult__subject__subject_short_name']

class TestResultAdmin(admin.ModelAdmin):
    search_fields = ['subject__subject_code', 'subject__subject_short_name']

class MOOCCourseAdmin(admin.ModelAdmin):
    search_fields = ['course_name']

class MOOCResultAdmin(admin.ModelAdmin):
    search_fields = ['course__course_name']

class IndividualProjectAdmin(admin.ModelAdmin):
    search_fields = ['subject__subject_code', 'subject__subject_short_name']

class GroupProjectAdmin(admin.ModelAdmin):
    search_fields = ['subject__subject_code', 'subject__subject_short_name']

class StudentSemesterRecordAdmin(admin.ModelAdmin):
    search_fields = ['student__enrolment_no', 'student__email']

admin.site.register(StaffDetail, StaffDetailAdmin)
admin.site.register(Weightage, WeightageAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(StudentDetail, StudentDetailAdmin)
admin.site.register(FacultyAllocation, FacultyAllocationAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(StudyResource, StudyResourceAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(RemedialTestResult, RemedialTestResultAdmin)
admin.site.register(TestResult, TestResultAdmin)
admin.site.register(MOOCCourse, MOOCCourseAdmin)
admin.site.register(MOOCResult, MOOCResultAdmin)
admin.site.register(IndividualProject, IndividualProjectAdmin)
admin.site.register(GroupProject, GroupProjectAdmin)
admin.site.register(StudentSemesterRecord, StudentSemesterRecordAdmin)
