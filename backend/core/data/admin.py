from django.contrib import admin  
from .models import StaffDetail, Weightage, Subject, Branch, StudentDetail, FacultyAllocation, Batch, StudyResource, Department, Attendance, RemedialTestResult, TestResult, MOOCCourse, MOOCResult, IndividualProject, GroupProject, StudentSemesterRecord


class SemesterSearch:
    def get_search_results(self, request, queryset, search_term):
        # Check if the search term matches a semester value
        if search_term.startswith('SEM='):
            semester = search_term.split('=')[1].strip()

            # Filter queryset based on the semester value
            queryset = queryset.filter(department__semester=semester)
            return queryset, True

        # If the search term doesn't match a semester value, perform the default search
        return super().get_search_results(request, queryset, search_term)

class RollNoSearch:
    def get_search_results(self, request, queryset, search_term):
        # Check if the search term matches a semester value
        if search_term.startswith('RollNo='):
            roll_no = search_term.split('=')[1].strip()

            # Filter queryset based on the semester value
            queryset = queryset.filter(studentsemesterrecord__roll_no=roll_no)
            return queryset, True

        # If the search term doesn't match a semester value, perform the default search
        return super().get_search_results(request, queryset, search_term)

class StaffDetailAdmin(admin.ModelAdmin):
    search_fields = ['email', 'short_name', 'first_name', 'last_name']

class WeightageAdmin(admin.ModelAdmin):
    search_fields = ['subject__subject_short_name', 'subject__subject_full_name', 'teaching_type', 'category']

class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['subject_code', 'subject_short_name', 'subject_full_name']

class BranchAdmin(admin.ModelAdmin):
    search_fields = ['branch_code', 'branch_short_name', 'branch_full_name']

class StudentDetailAdmin(admin.ModelAdmin):
    search_fields = ['email', 'enrolment_no', 'first_name', 'last_name', 'year_joined']
    search_fields = ['name', 'year', 'semester']
    def get_search_results(self, request, queryset, search_term):
        # Check if the search term matches a semester value
        if search_term.startswith('year_joined='):
            year = search_term.split('=')[1].strip()

            # Filter queryset based on the semester value
            queryset = queryset.filter(year_joined=year)
            return queryset, True

        # If the search term doesn't match a semester value, perform the default search
        return super().get_search_results(request, queryset, search_term)



class FacultyAllocationAdmin(admin.ModelAdmin):
    search_fields = ['faculty__email', 'faculty__first_name', 'faculty__last_name', 'subject__subject_code', 'subject__subject_short_name']

class BatchAdmin(SemesterSearch,admin.ModelAdmin):
    search_fields = ['name', 'department__name', 'department__year', 'department__semester']
    
class StudyResourceAdmin(admin.ModelAdmin):
    search_fields = ['name', 'subject__subject_full_name', 'subject__subject_short_name']

class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ['name', 'year', 'semester']
    def get_search_results(self, request, queryset, search_term):
        # Check if the search term matches a semester value
        if search_term.startswith('SEM='):
            semester = search_term.split('=')[1].strip()

            # Filter queryset based on the semester value
            queryset = queryset.filter(semester=semester)
            return queryset, True

        # If the search term doesn't match a semester value, perform the default search
        return super().get_search_results(request, queryset, search_term)

class AttendanceAdmin(RollNoSearch, admin.ModelAdmin):
    search_fields = ['studentsemesterrecord__student__enrolment_no', 'studentsemesterrecord__roll_no', 'studentsemesterrecord__student__email', 'date']
    
class RemedialTestResultAdmin(admin.ModelAdmin):
    search_fields = ['testresult__subject__subject_code', 'testresult__subject__subject_short_name', 'testresult__studentsemesterrecord__student__enrolment_no']

class TestResultAdmin(RollNoSearch, admin.ModelAdmin):
    search_fields = ['subject__subject_code', 'subject__subject_short_name', 'subject__subject_full_name', 'studentsemesterrecord__student__enrolment_no', 'studentsemesterrecord__roll_no']
    
class MOOCCourseAdmin(admin.ModelAdmin):
    search_fields = ['course_name']

class MOOCResultAdmin(RollNoSearch, admin.ModelAdmin):
    search_fields = ['course__course_name',  'studentsemesterrecord__student__enrolment_no', 'studentsemesterrecord__roll_no']
  
class IndividualProjectAdmin(RollNoSearch, admin.ModelAdmin):
    search_fields = ['subject__subject_code', 'subject__subject_short_name', 'subject__subject_full_name', 'studentsemesterrecord__student__enrolment_no', 'studentsemesterrecord__roll_no']
 
class GroupProjectAdmin(RollNoSearch, admin.ModelAdmin):
    search_fields = ['subject__subject_code', 'subject__subject_short_name', 'studentsemesterrecord__roll_no']
   
class StudentSemesterRecordAdmin(SemesterSearch, admin.ModelAdmin):
    search_fields = ['student__enrolment_no', 'student__email', 'roll_no', 'department__semester']
    def get_search_results(self, request, queryset, search_term):
        # Check if the search term matches a semester value
        if search_term.startswith('RollNo='):
            roll_no = search_term.split('=')[1].strip()
            # Filter queryset based on the semester value
            queryset = queryset.filter(roll_no=roll_no)
            return queryset, True

        # If the search term doesn't match a semester value, perform the default search
        return super().get_search_results(request, queryset, search_term)


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
