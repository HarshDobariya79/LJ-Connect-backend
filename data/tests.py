import json

from django.test import TestCase

from .models import (
    Attendance,
    Batch,
    Branch,
    Department,
    FacultyAllocation,
    GroupProject,
    IndividualProject,
    MOOCCourse,
    MOOCResult,
    RemedialTestResult,
    StaffDetail,
    StudentDetail,
    StudentSemesterRecord,
    StudyResource,
    Subject,
    TestResult,
    Weightage,
)
from .utils import permissions_assign


class StaffDetailTestCase(TestCase):
    fixtures = [
        "data/test_fixtures/StaffDetailTestCase.json",
    ]

    def test_create_staff(self):
        StaffDetail.objects.create(
            email="staff5@ljku.edu.in",
            first_name="fname5",
            last_name="lastname5",
            gender="M",
            birth_date="1990-01-01",
            mobile_number="+911234567891",
            category="T",
            active=True,
        )

        self.assertEqual(StaffDetail.objects.count(), 5)

    def test_read_staff(self):
        staff_from_db = StaffDetail.objects.get(email="staff1@ljku.edu.in")

        self.assertEqual(staff_from_db.first_name, "fname1")
        self.assertEqual(staff_from_db.last_name, "lname1")
        self.assertEqual(staff_from_db.gender, "M")

    def test_update_staff(self):
        staff = StaffDetail.objects.get(email="staff2@ljku.edu.in")
        staff.first_name = "fname2new"
        staff.save()

        staff_from_db = StaffDetail.objects.get(email="staff2@ljku.edu.in")
        self.assertEqual(staff_from_db.first_name, "fname2new")

    def test_delete_staff(self):
        staff = StaffDetail.objects.get(email="staff3@ljku.edu.in")
        staff.delete()

        self.assertEqual(StaffDetail.objects.count(), 3)
        self.assertFalse(StudentSemesterRecord.objects.filter(pk=1).exists())


class PermissionAutomationTestCase(TestCase):
    fixtures = [
        "data/test_fixtures/PermissionAutomationTestCase.json",
    ]

    def test_model_data_count(self):
        self.assertEqual(Department.objects.count(), 1)
        self.assertEqual(Batch.objects.count(), 2)
        self.assertEqual(StaffDetail.objects.count(), 3)
        self.assertEqual(StudentDetail.objects.count(), 2)

    def test_current_permissions(self):
        staff1 = StaffDetail.objects.get(email="staff1@ljku.edu.in")
        staff2 = StaffDetail.objects.get(email="staff2@ljku.edu.in")
        staff3 = StaffDetail.objects.get(email="staff3@ljku.edu.in")

        self.assertEqual(
            json.dumps(staff1.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B1": {"mooc": {"read": true, "create": true, "delete": false, "update": false}, "project": {"read": true, "create": true, "delete": false, "update": true}, "attendance": {"read": true, "create": true, "delete": false, "update": false}, "test_result": {"read": true, "create": true, "delete": false, "update": false}}}}}}',
        )

        self.assertEqual(
            json.dumps(staff2.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B2": {"mooc": {"read": true, "create": true, "delete": false, "update": false}, "project": {"read": true, "create": true, "delete": false, "update": true}, "attendance": {"read": true, "create": true, "delete": false, "update": false}, "test_result": {"read": true, "create": true, "delete": false, "update": false}}}}}}',
        )

        self.assertEqual(
            json.dumps(staff3.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B1": {"mooc": {"read": true, "create": true, "delete": true, "update": true}, "project": {"read": true, "create": true, "delete": true, "update": true}, "attendance": {"read": true, "create": true, "delete": true, "update": true}, "test_result": {"read": true, "create": true, "delete": true, "update": true}}, "B2": {"mooc": {"read": true, "create": true, "delete": true, "update": true}, "project": {"read": true, "create": true, "delete": true, "update": true}, "attendance": {"read": true, "create": true, "delete": true, "update": true}, "test_result": {"read": true, "create": true, "delete": true, "update": true}}}}}}',
        )

    def test_change_hod(self):
        staff1 = StaffDetail.objects.get(email="staff1@ljku.edu.in")
        department = Department.objects.all()[0]

        department.hod = staff1
        department.save()

        staff1 = StaffDetail.objects.get(email="staff1@ljku.edu.in")
        staff2 = StaffDetail.objects.get(email="staff2@ljku.edu.in")
        staff3 = StaffDetail.objects.get(email="staff3@ljku.edu.in")

        self.assertEqual(
            json.dumps(staff1.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B1": {"mooc": {"read": true, "create": true, "delete": true, "update": true}, "project": {"read": true, "create": true, "delete": true, "update": true}, "attendance": {"read": true, "create": true, "delete": true, "update": true}, "test_result": {"read": true, "create": true, "delete": true, "update": true}}, "B2": {"mooc": {"read": true, "create": true, "delete": true, "update": true}, "project": {"read": true, "create": true, "delete": true, "update": true}, "attendance": {"read": true, "create": true, "delete": true, "update": true}, "test_result": {"read": true, "create": true, "delete": true, "update": true}}}}}}',
        )

        self.assertEqual(
            json.dumps(staff2.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B2": {"mooc": {"read": true, "create": true, "delete": false, "update": false}, "project": {"read": true, "create": true, "delete": false, "update": true}, "attendance": {"read": true, "create": true, "delete": false, "update": false}, "test_result": {"read": true, "create": true, "delete": false, "update": false}}}}}}',
        )

        self.assertEqual(json.dumps(staff3.permissions), "{}")

        department.hod = staff2
        department.save()

        staff1 = StaffDetail.objects.get(email="staff1@ljku.edu.in")
        staff2 = StaffDetail.objects.get(email="staff2@ljku.edu.in")
        staff3 = StaffDetail.objects.get(email="staff3@ljku.edu.in")

        self.assertEqual(
            json.dumps(staff1.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B1": {"mooc": {"read": true, "create": true, "delete": false, "update": false}, "project": {"read": true, "create": true, "delete": false, "update": true}, "attendance": {"read": true, "create": true, "delete": false, "update": false}, "test_result": {"read": true, "create": true, "delete": false, "update": false}}}}}}',
        )

        self.assertEqual(
            json.dumps(staff2.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B1": {"mooc": {"read": true, "create": true, "delete": true, "update": true}, "project": {"read": true, "create": true, "delete": true, "update": true}, "attendance": {"read": true, "create": true, "delete": true, "update": true}, "test_result": {"read": true, "create": true, "delete": true, "update": true}}, "B2": {"mooc": {"read": true, "create": true, "delete": true, "update": true}, "project": {"read": true, "create": true, "delete": true, "update": true}, "attendance": {"read": true, "create": true, "delete": true, "update": true}, "test_result": {"read": true, "create": true, "delete": true, "update": true}}}}}}',
        )

        self.assertEqual(json.dumps(staff3.permissions), "{}")

        department.hod = staff3
        department.save()

        staff1 = StaffDetail.objects.get(email="staff1@ljku.edu.in")
        staff2 = StaffDetail.objects.get(email="staff2@ljku.edu.in")
        staff3 = StaffDetail.objects.get(email="staff3@ljku.edu.in")

        self.assertEqual(
            json.dumps(staff1.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B1": {"mooc": {"read": true, "create": true, "delete": false, "update": false}, "project": {"read": true, "create": true, "delete": false, "update": true}, "attendance": {"read": true, "create": true, "delete": false, "update": false}, "test_result": {"read": true, "create": true, "delete": false, "update": false}}}}}}',
        )

        self.assertEqual(
            json.dumps(staff2.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B2": {"mooc": {"read": true, "create": true, "delete": false, "update": false}, "project": {"read": true, "create": true, "delete": false, "update": true}, "attendance": {"read": true, "create": true, "delete": false, "update": false}, "test_result": {"read": true, "create": true, "delete": false, "update": false}}}}}}',
        )

        self.assertEqual(
            json.dumps(staff3.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B1": {"mooc": {"read": true, "create": true, "delete": true, "update": true}, "project": {"read": true, "create": true, "delete": true, "update": true}, "attendance": {"read": true, "create": true, "delete": true, "update": true}, "test_result": {"read": true, "create": true, "delete": true, "update": true}}, "B2": {"mooc": {"read": true, "create": true, "delete": true, "update": true}, "project": {"read": true, "create": true, "delete": true, "update": true}, "attendance": {"read": true, "create": true, "delete": true, "update": true}, "test_result": {"read": true, "create": true, "delete": true, "update": true}}}}}}',
        )

    def test_change_batches(self):
        department = Department.objects.all()[0]
        batch_b2 = Batch.objects.get(name="B2")

        department.batch.remove(batch_b2)
        staff1 = StaffDetail.objects.get(email="staff1@ljku.edu.in")
        staff2 = StaffDetail.objects.get(email="staff2@ljku.edu.in")
        staff3 = StaffDetail.objects.get(email="staff3@ljku.edu.in")

        self.assertEqual(Batch.objects.count(), 1)

        self.assertEqual(
            json.dumps(staff1.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B1": {"mooc": {"read": true, "create": true, "delete": false, "update": false}, "project": {"read": true, "create": true, "delete": false, "update": true}, "attendance": {"read": true, "create": true, "delete": false, "update": false}, "test_result": {"read": true, "create": true, "delete": false, "update": false}}}}}}',
        )

        self.assertEqual(json.dumps(staff2.permissions), "{}")

        self.assertEqual(
            json.dumps(staff3.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B1": {"mooc": {"read": true, "create": true, "delete": true, "update": true}, "project": {"read": true, "create": true, "delete": true, "update": true}, "attendance": {"read": true, "create": true, "delete": true, "update": true}, "test_result": {"read": true, "create": true, "delete": true, "update": true}}}}}}',
        )

        batch_b3 = Batch(name="B3")
        batch_b3.save()
        batch_b3.faculty.add(FacultyAllocation.objects.all()[0])
        batch_b3.student.add(StudentDetail.objects.get(email="student2@ljku.edu.in"))
        department.batch.add(batch_b3)
        staff1 = StaffDetail.objects.get(email="staff1@ljku.edu.in")
        staff2 = StaffDetail.objects.get(email="staff2@ljku.edu.in")
        staff3 = StaffDetail.objects.get(email="staff3@ljku.edu.in")

        self.assertEqual(
            json.dumps(staff1.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B1": {"mooc": {"read": true, "create": true, "delete": false, "update": false}, "project": {"read": true, "create": true, "delete": false, "update": true}, "attendance": {"read": true, "create": true, "delete": false, "update": false}, "test_result": {"read": true, "create": true, "delete": false, "update": false}}, "B3": {"mooc": {"read": true, "create": true, "delete": false, "update": false}, "project": {"read": true, "create": true, "delete": false, "update": true}, "attendance": {"read": true, "create": true, "delete": false, "update": false}, "test_result": {"read": true, "create": true, "delete": false, "update": false}}}}}}',
        )

        self.assertEqual(json.dumps(staff2.permissions), "{}")

        self.assertEqual(
            json.dumps(staff3.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B1": {"mooc": {"read": true, "create": true, "delete": true, "update": true}, "project": {"read": true, "create": true, "delete": true, "update": true}, "attendance": {"read": true, "create": true, "delete": true, "update": true}, "test_result": {"read": true, "create": true, "delete": true, "update": true}}, "B3": {"mooc": {"read": true, "create": true, "delete": true, "update": true}, "project": {"read": true, "create": true, "delete": true, "update": true}, "attendance": {"read": true, "create": true, "delete": true, "update": true}, "test_result": {"read": true, "create": true, "delete": true, "update": true}}}}}}',
        )

    def test_delete_department(self):
        department = Department.objects.all()[0]
        department.delete()
        staff1 = StaffDetail.objects.get(email="staff1@ljku.edu.in")
        staff2 = StaffDetail.objects.get(email="staff2@ljku.edu.in")
        staff3 = StaffDetail.objects.get(email="staff3@ljku.edu.in")

        self.assertEqual(json.dumps(staff1.permissions), "{}")
        self.assertEqual(json.dumps(staff2.permissions), "{}")
        self.assertEqual(json.dumps(staff3.permissions), "{}")

    def test_modify_batch_faculty(self):
        batch_b1 = Batch.objects.get(name="B1")
        staff2 = FacultyAllocation.objects.get(faculty__email="staff2@ljku.edu.in")
        staff3 = FacultyAllocation.objects.get(faculty__email="staff3@ljku.edu.in")
        batch_b1.faculty.add(staff2)
        batch_b1.faculty.add(staff3)
        staff1 = StaffDetail.objects.get(email="staff1@ljku.edu.in")
        staff2 = StaffDetail.objects.get(email="staff2@ljku.edu.in")
        staff3 = StaffDetail.objects.get(email="staff3@ljku.edu.in")

        self.assertEqual(
            json.dumps(staff1.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B1": {"mooc": {"read": true, "create": true, "delete": false, "update": false}, "project": {"read": true, "create": true, "delete": false, "update": true}, "attendance": {"read": true, "create": true, "delete": false, "update": false}, "test_result": {"read": true, "create": true, "delete": false, "update": false}}}}}}',
        )

        self.assertEqual(
            json.dumps(staff2.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B1": {"mooc": {"read": true, "create": true, "delete": false, "update": false}, "project": {"read": true, "create": true, "delete": false, "update": true}, "attendance": {"read": true, "create": true, "delete": false, "update": false}, "test_result": {"read": true, "create": true, "delete": false, "update": false}}, "B2": {"mooc": {"read": true, "create": true, "delete": false, "update": false}, "project": {"read": true, "create": true, "delete": false, "update": true}, "attendance": {"read": true, "create": true, "delete": false, "update": false}, "test_result": {"read": true, "create": true, "delete": false, "update": false}}}}}}',
        )

        self.assertEqual(
            json.dumps(staff3.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B1": {"mooc": {"read": true, "create": true, "delete": true, "update": true}, "project": {"read": true, "create": true, "delete": true, "update": true}, "attendance": {"read": true, "create": true, "delete": true, "update": true}, "test_result": {"read": true, "create": true, "delete": true, "update": true}}, "B2": {"mooc": {"read": true, "create": true, "delete": true, "update": true}, "project": {"read": true, "create": true, "delete": true, "update": true}, "attendance": {"read": true, "create": true, "delete": true, "update": true}, "test_result": {"read": true, "create": true, "delete": true, "update": true}}}}}}',
        )

        staff2 = FacultyAllocation.objects.get(faculty__email="staff2@ljku.edu.in")
        batch_b1.faculty.remove(staff2)
        staff1 = StaffDetail.objects.get(email="staff1@ljku.edu.in")
        staff2 = StaffDetail.objects.get(email="staff2@ljku.edu.in")
        staff3 = StaffDetail.objects.get(email="staff3@ljku.edu.in")

        self.assertEqual(
            json.dumps(staff1.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B1": {"mooc": {"read": true, "create": true, "delete": false, "update": false}, "project": {"read": true, "create": true, "delete": false, "update": true}, "attendance": {"read": true, "create": true, "delete": false, "update": false}, "test_result": {"read": true, "create": true, "delete": false, "update": false}}}}}}',
        )

        self.assertEqual(
            json.dumps(staff2.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B2": {"mooc": {"read": true, "create": true, "delete": false, "update": false}, "project": {"read": true, "create": true, "delete": false, "update": true}, "attendance": {"read": true, "create": true, "delete": false, "update": false}, "test_result": {"read": true, "create": true, "delete": false, "update": false}}}}}}',
        )

        self.assertEqual(
            json.dumps(staff3.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B1": {"mooc": {"read": true, "create": true, "delete": true, "update": true}, "project": {"read": true, "create": true, "delete": true, "update": true}, "attendance": {"read": true, "create": true, "delete": true, "update": true}, "test_result": {"read": true, "create": true, "delete": true, "update": true}}, "B2": {"mooc": {"read": true, "create": true, "delete": true, "update": true}, "project": {"read": true, "create": true, "delete": true, "update": true}, "attendance": {"read": true, "create": true, "delete": true, "update": true}, "test_result": {"read": true, "create": true, "delete": true, "update": true}}}}}}',
        )

    def test_delete_batch(self):
        batch_b1 = Batch.objects.get(name="B1")
        batch_b1.delete()
        staff1 = StaffDetail.objects.get(email="staff1@ljku.edu.in")
        staff2 = StaffDetail.objects.get(email="staff2@ljku.edu.in")
        staff3 = StaffDetail.objects.get(email="staff3@ljku.edu.in")

        self.assertEqual(json.dumps(staff1.permissions), "{}")

        self.assertEqual(
            json.dumps(staff2.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B2": {"mooc": {"read": true, "create": true, "delete": false, "update": false}, "project": {"read": true, "create": true, "delete": false, "update": true}, "attendance": {"read": true, "create": true, "delete": false, "update": false}, "test_result": {"read": true, "create": true, "delete": false, "update": false}}}}}}',
        )

        self.assertEqual(
            json.dumps(staff3.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B2": {"mooc": {"read": true, "create": true, "delete": true, "update": true}, "project": {"read": true, "create": true, "delete": true, "update": true}, "attendance": {"read": true, "create": true, "delete": true, "update": true}, "test_result": {"read": true, "create": true, "delete": true, "update": true}}}}}}',
        )

    def test_department_lock_unlock(self):
        department = Department.objects.all()[0]

        department.locked = True
        department.save()

        staff1 = StaffDetail.objects.get(email="staff1@ljku.edu.in")
        staff2 = StaffDetail.objects.get(email="staff2@ljku.edu.in")
        staff3 = StaffDetail.objects.get(email="staff3@ljku.edu.in")

        self.assertEqual(
            json.dumps(staff1.permissions),
            "{}",
        )

        self.assertEqual(
            json.dumps(staff2.permissions),
            "{}",
        )

        self.assertEqual(
            json.dumps(staff3.permissions),
            "{}",
        )

        department.locked = False
        department.save()

        staff1 = StaffDetail.objects.get(email="staff1@ljku.edu.in")
        staff2 = StaffDetail.objects.get(email="staff2@ljku.edu.in")
        staff3 = StaffDetail.objects.get(email="staff3@ljku.edu.in")

        self.assertEqual(
            json.dumps(staff1.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B1": {"mooc": {"read": true, "create": true, "delete": false, "update": false}, "project": {"read": true, "create": true, "delete": false, "update": true}, "attendance": {"read": true, "create": true, "delete": false, "update": false}, "test_result": {"read": true, "create": true, "delete": false, "update": false}}}}}}',
        )

        self.assertEqual(
            json.dumps(staff2.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B2": {"mooc": {"read": true, "create": true, "delete": false, "update": false}, "project": {"read": true, "create": true, "delete": false, "update": true}, "attendance": {"read": true, "create": true, "delete": false, "update": false}, "test_result": {"read": true, "create": true, "delete": false, "update": false}}}}}}',
        )

        self.assertEqual(
            json.dumps(staff3.permissions),
            '{"2024-25": {"5": {"DEPT_1": {"B1": {"mooc": {"read": true, "create": true, "delete": true, "update": true}, "project": {"read": true, "create": true, "delete": true, "update": true}, "attendance": {"read": true, "create": true, "delete": true, "update": true}, "test_result": {"read": true, "create": true, "delete": true, "update": true}}, "B2": {"mooc": {"read": true, "create": true, "delete": true, "update": true}, "project": {"read": true, "create": true, "delete": true, "update": true}, "attendance": {"read": true, "create": true, "delete": true, "update": true}, "test_result": {"read": true, "create": true, "delete": true, "update": true}}}}}}',
        )


class PermissionsAssignUtil(TestCase):
    temp = {"a": {"b": 1}}

    def test_base_assign(self):
        permissions_assign(self.temp, ["c"], 2)
        self.assertEqual(self.temp, {"a": {"b": 1}, "c": 2})

    def test_nested_assign(self):
        permissions_assign(self.temp, ["a", "c", "d"], 5)
        self.assertEqual(self.temp, {"a": {"b": 1, "c": {"d": 5}}, "c": 2})


class WeightageTestCase(TestCase):
    fixtures = [
        "data/test_fixtures/WeightageTestCase.json",
    ]

    def test_create_weightage(self):
        Weightage.objects.create(
            teaching_type="T",
            category="MCQ",
            percentage_weightage=30,
            marks_weightage=40,
        )

        self.assertEqual(Weightage.objects.count(), 4)

    def test_read_weightage(self):
        weightage_from_db = Weightage.objects.get(teaching_type="T", category="MCQ")

        self.assertEqual(weightage_from_db.percentage_weightage, 23)
        self.assertEqual(weightage_from_db.marks_weightage, 13)

    def test_update_weightage(self):
        weightage = Weightage.objects.get(teaching_type="T", category="MCQ")
        weightage.percentage_weightage = 50
        weightage.save()

        weightage_from_db = Weightage.objects.get(teaching_type="T", category="MCQ")
        self.assertEqual(weightage_from_db.percentage_weightage, 50)

    def test_delete_weightage(self):
        weightage_to_delete = Weightage.objects.get(pk=3)
        weightage_to_delete.delete()

        self.assertEqual(Weightage.objects.count(), 2)
        self.assertFalse(Weightage.objects.filter(pk=3).exists())


class BranchTestCase(TestCase):
    fixtures = ["data/test_fixtures/BranchTestCase.json"]

    def test_create_branch(self):
        new_branch = Branch.objects.create(
            branch_code="2345567861",
            branch_short_name="ME",
            branch_full_name="Mechanical Engineering",
            available=True,
        )

        self.assertEqual(Branch.objects.count(), 3)

    def test_read_branch(self):
        branch = Branch.objects.get(branch_code="2654862341")

        self.assertEqual(branch.branch_short_name, "CSE")
        self.assertEqual(branch.branch_full_name, "Computer Science and Engineering")
        self.assertTrue(branch.available)

    def test_update_branch(self):
        branch = Branch.objects.get(branch_code="2654862341")

        branch.branch_short_name = "ECE"
        branch.save()

        updated_branch = Branch.objects.get(branch_code="2654862341")

        self.assertEqual(updated_branch.branch_short_name, "ECE")

    def test_delete_branch(self):
        branch = Branch.objects.get(branch_code="2654862341")

        branch.delete()

        self.assertEqual(Branch.objects.count(), 1)
        self.assertFalse(Branch.objects.filter(branch_code="2654862341").exists())


class SubjectTestCase(TestCase):
    fixtures = [
        "data/test_fixtures/SubjectTestCase.json",
        "data/test_fixtures/WeightageTestCase.json",
    ]

    def test_create_subject(self):
        Subject.objects.create(
            subject_code="123456",
            subject_short_name="SUB3",
            subject_full_name="subject3",
            total_credit=5,
            theory_credit=3,
            tutorial_credit=1,
            practical_credit=1,
        )

        self.assertEqual(Subject.objects.count(), 4)

    def test_read_subject(self):
        subject_from_db = Subject.objects.get(subject_code="12546525")

        self.assertEqual(subject_from_db.subject_short_name, "FCSP-2")
        self.assertEqual(subject_from_db.total_credit, 5)

    def test_update_subject(self):
        subject = Subject.objects.get(subject_code="12546525")
        subject.subject_short_name = "FCSP-2-NEW"
        subject.save()

        subject_from_db = Subject.objects.get(subject_code="12546525")
        self.assertEqual(subject_from_db.subject_short_name, "FCSP-2-NEW")

    def test_delete_subject(self):
        subject = Subject.objects.get(subject_code="26541254")
        subject.delete()

        self.assertEqual(Subject.objects.count(), 2)
        self.assertFalse(Subject.objects.filter(subject_code="26541254").exists())


class StudentDetailTestCase(TestCase):
    fixtures = [
        "data/test_fixtures/StudentDetailTestCase.json",
        "data/test_fixtures/BranchTestCase.json",
    ]

    def test_create_student(self):
        StudentDetail.objects.create(
            enrolment_no="25468521268",
            email="student4@ljku.edu.in",
            first_name="sfname4",
            last_name="slname4",
            gender="M",
            birth_date="2004-04-04",
            mobile_number="+1112223334",
            branch=Branch.objects.all()[0],
        )

        self.assertEqual(StudentDetail.objects.count(), 4)

    def test_read_student(self):
        student_from_db = StudentDetail.objects.get(email="student1@ljku.edu.in")

        self.assertEqual(student_from_db.first_name, "sfname1")
        self.assertEqual(student_from_db.last_name, "slname1")
        self.assertEqual(student_from_db.gender, "M")

    def test_update_student(self):
        student = StudentDetail.objects.get(email="student2@ljku.edu.in")

        student.first_name = "sfname1new"
        student.save()

        student_from_db = StudentDetail.objects.get(email="student2@ljku.edu.in")

        self.assertEqual(student_from_db.first_name, "sfname1new")

    def test_delete_student(self):
        student = StudentDetail.objects.get(email="student2@ljku.edu.in")

        student.delete()

        self.assertEqual(StudentDetail.objects.count(), 2)
        self.assertFalse(
            StudentDetail.objects.filter(email="student2@ljku.edu.in").exists()
        )


class FacultyAllocationTestCase(TestCase):
    fixtures = [
        "data/test_fixtures/StaffDetailTestCase.json",
        "data/test_fixtures/SubjectTestCase.json",
        "data/test_fixtures/FacultyAllocationTestCase.json",
    ]

    def test_create_faculty_allocation(self):
        faculty = StaffDetail.objects.get(email="staff4@ljku.edu.in")
        subject = Subject.objects.get(subject_code="23344556")
        faculty_allocation = FacultyAllocation.objects.create(
            faculty=faculty,
            subject=subject,
        )

        self.assertEqual(FacultyAllocation.objects.count(), 4)

    def test_read_faculty_allocation(self):
        faculty_allocation = FacultyAllocation.objects.get(pk=1)

        self.assertEqual(faculty_allocation.faculty.email, "staff1@ljku.edu.in")
        self.assertEqual(faculty_allocation.subject.subject_code, "26541254")

    def test_update_faculty_allocation(self):
        faculty_allocation = FacultyAllocation.objects.get(pk=1)
        new_subject = Subject.objects.get(subject_code="23344556")

        faculty_allocation.subject = new_subject
        faculty_allocation.save()

        updated_faculty_allocation = FacultyAllocation.objects.get(pk=1)

        self.assertEqual(updated_faculty_allocation.subject.subject_code, "23344556")

    def test_delete_faculty_allocation(self):
        faculty_allocation = FacultyAllocation.objects.get(pk=1)

        faculty_allocation.delete()

        self.assertEqual(FacultyAllocation.objects.count(), 2)
        self.assertFalse(FacultyAllocation.objects.filter(pk=1).exists())


class BatchTestCase(TestCase):
    fixtures = [
        "data/test_fixtures/BatchTestCase.json",
        "data/test_fixtures/BranchTestCase.json",
        "data/test_fixtures/FacultyAllocationTestCase.json",
        "data/test_fixtures/StaffDetailTestCase.json",
        "data/test_fixtures/StudentDetailTestCase.json",
        "data/test_fixtures/SubjectTestCase.json",
    ]

    def test_create_batch(self):
        batch = Batch.objects.create(name="B3")

        self.assertEqual(Batch.objects.count(), 3)
        self.assertTrue(Batch.objects.filter(name="B3").exists())

    def test_read_batch(self):
        batch = Batch.objects.get(name="B1")

        self.assertEqual(batch.name, "B1")

    def test_update_batch(self):
        batch = Batch.objects.get(name="B2")

        batch.name = "B2_updated"
        batch.save()

        updated_batch = Batch.objects.get(pk=batch.pk)

        self.assertEqual(updated_batch.name, "B2_updated")

    def test_delete_batch(self):
        batch = Batch.objects.get(name="B1")

        batch.delete()

        self.assertFalse(Batch.objects.filter(name="B1").exists())

    def test_add_faculty_to_batch(self):
        batch = Batch.objects.get(name="B1")
        faculty_allocation = FacultyAllocation.objects.get(pk=1)

        batch.faculty.add(faculty_allocation)

        updated_batch = Batch.objects.get(pk=batch.pk)

        self.assertEqual(updated_batch.faculty.count(), 1)
        self.assertTrue(updated_batch.faculty.filter(pk=faculty_allocation.pk).exists())

    def test_update_faculty_in_batch(self):
        batch = Batch.objects.get(pk=1)
        new_faculty_allocation = FacultyAllocation.objects.get(pk=2)

        self.assertEqual(batch.faculty.count(), 1)
        self.assertTrue(batch.faculty.filter(pk=1).exists())
        self.assertFalse(batch.faculty.filter(pk=2).exists())

        batch.faculty.set([new_faculty_allocation])

        self.assertEqual(batch.faculty.count(), 1)
        self.assertFalse(batch.faculty.filter(pk=1).exists())
        self.assertTrue(batch.faculty.filter(pk=2).exists())

    def test_remove_faculty_from_batch(self):
        batch = Batch.objects.get(name="B2")
        faculty_allocation = FacultyAllocation.objects.get(pk=2)

        batch.faculty.remove(faculty_allocation)

        updated_batch = Batch.objects.get(pk=batch.pk)

        self.assertEqual(updated_batch.faculty.count(), 0)
        self.assertFalse(
            updated_batch.faculty.filter(pk=faculty_allocation.pk).exists()
        )

    def test_add_student_to_batch(self):
        batch = Batch.objects.get(name="B1")
        student = StudentDetail.objects.get(email="student1@ljku.edu.in")

        batch.student.add(student)

        updated_batch = Batch.objects.get(pk=batch.pk)

        self.assertEqual(updated_batch.student.count(), 1)
        self.assertTrue(updated_batch.student.filter(pk=student.pk).exists())

    def test_update_student_in_batch(self):
        batch = Batch.objects.get(pk=2)
        new_student = StudentDetail.objects.get(pk="25468521265")

        self.assertEqual(batch.student.count(), 1)
        self.assertTrue(batch.student.filter(pk="25468521266").exists())
        self.assertFalse(batch.student.filter(pk="25468521265").exists())

        batch.student.set([new_student])

        self.assertEqual(batch.student.count(), 1)
        self.assertFalse(batch.student.filter(pk="25468521266").exists())
        self.assertTrue(batch.student.filter(pk="25468521265").exists())

    def test_remove_student_from_batch(self):
        batch = Batch.objects.get(name="B2")
        student = StudentDetail.objects.get(email="student2@ljku.edu.in")

        batch.student.remove(student)

        updated_batch = Batch.objects.get(pk=batch.pk)

        self.assertEqual(updated_batch.student.count(), 0)
        self.assertFalse(updated_batch.student.filter(pk=student.pk).exists())


class StudyResourceTestCase(TestCase):
    fixtures = [
        "data/test_fixtures/StudyResourceTestCase.json",
        "data/test_fixtures/SubjectTestCase.json",
        "data/test_fixtures/WeightageTestCase.json",
    ]

    def test_create_study_resource(self):
        subject = Subject.objects.get(subject_short_name="DM")
        study_resource = StudyResource.objects.create(
            subject=subject,
            name="Study Resource 1",
            resource_type="QB",
            file="study_resources/a.pdf",
        )

        self.assertEqual(StudyResource.objects.count(), 2)
        self.assertTrue(
            StudyResource.objects.filter(
                subject=subject,
                name="Study Resource 1",
                resource_type="QB",
                file="study_resources/a.pdf",
            ).exists()
        )

    def test_read_study_resource(self):
        study_resource = StudyResource.objects.get(name="resource_name")

        self.assertEqual(study_resource.name, "resource_name")

    def test_update_study_resource(self):
        study_resource = StudyResource.objects.get(name="resource_name")

        study_resource.name = "Study Resource 1 Updated"
        study_resource.save()

        updated_study_resource = StudyResource.objects.get(pk=study_resource.pk)

        self.assertEqual(updated_study_resource.name, "Study Resource 1 Updated")

    def test_delete_study_resource(self):
        study_resource = StudyResource.objects.get(name="resource_name")

        study_resource.delete()

        self.assertEqual(StudyResource.objects.count(), 0)
        self.assertFalse(StudyResource.objects.filter(name="resource_name").exists())


class DepartmentTestCase(TestCase):
    fixtures = [
        "data/test_fixtures/DepartmentTestCase.json",
        "data/test_fixtures/StudyResourceTestCase.json",
        "data/test_fixtures/StaffDetailTestCase.json",
        "data/test_fixtures/BranchTestCase.json",
        "data/test_fixtures/BatchTestCase.json",
        "data/test_fixtures/FacultyAllocationTestCase.json",
        "data/test_fixtures/SubjectTestCase.json",
        "data/test_fixtures/WeightageTestCase.json",
        "data/test_fixtures/StudentDetailTestCase.json",
        "data/test_fixtures/BranchTestCase.json",
    ]

    def test_create_department(self):
        staff = StaffDetail.objects.get(email="staff1@ljku.edu.in")
        department = Department.objects.create(
            year="2023-24",
            semester="2",
            name="DEPT_2",
            hod=staff,
        )

        self.assertEqual(Department.objects.count(), 2)
        self.assertTrue(
            Department.objects.filter(
                year="2023-24",
                semester="2",
                name="DEPT_2",
                hod=staff,
            ).exists()
        )

    def test_read_department(self):
        department = Department.objects.get(name="DEPT_1")
        self.assertEqual(department.name, "DEPT_1")

    def test_update_department(self):
        department = Department.objects.get(name="DEPT_1")

        department.name = "DEPT_1_updated"
        department.save()

        updated_department = Department.objects.get(pk=department.pk)

        self.assertEqual(updated_department.name, "DEPT_1_updated")

    def test_delete_department(self):
        department = Department.objects.get(name="DEPT_1")

        department.delete()

        self.assertEqual(Department.objects.count(), 0)
        self.assertFalse(Department.objects.filter(name="DEPT_1").exists())

    def test_add_batch_to_department(self):
        department = Department.objects.get(name="DEPT_1")

        batch = Batch.objects.create(name="B3")

        department.batch.add(batch)

        updated_department = Department.objects.get(pk=department.pk)

        self.assertEqual(updated_department.batch.count(), 3)
        self.assertTrue(updated_department.batch.filter(pk=department.pk).exists())

    def test_update_batch_to_department(self):
        department = Department.objects.get(name="DEPT_1")
        existing_batch_department = department.batch.first()

        existing_batch_department.name = "new B1"

        existing_batch_department.save()

        updated_batch_department = Batch.objects.get(pk=existing_batch_department.pk)

        self.assertEqual(updated_batch_department.name, "new B1")

    def test_remove_batch_to_department(self):
        department = Department.objects.get(name="DEPT_1")
        batch = Batch.objects.get(name="B1")

        department.batch.remove(batch)

        updated_department = Department.objects.get(pk=department.pk)
        self.assertEqual(updated_department.batch.count(), 1)
        self.assertFalse(updated_department.batch.filter(pk=department.pk).exists())

    def test_add_studyresource_to_department(self):
        department = Department.objects.get(name="DEPT_1")

        subject = Subject.objects.get(subject_short_name="DM")
        study_resource = StudyResource.objects.create(
            subject=subject,
            name="Study Resource 1",
            resource_type="QB",
            file="study_resources/QB_DM_SEM-IV_2023.pdf",
        )

        department.study_resource.add(study_resource)

        updated_department = Department.objects.get(pk=department.pk)

        self.assertEqual(updated_department.study_resource.count(), 1)
        self.assertTrue(
            updated_department.study_resource.filter(pk=study_resource.pk).exists()
        )

    def test_remove_studyresource_to_department(self):
        department = Department.objects.get(name="DEPT_1")
        study_resource = StudyResource.objects.get(pk=2)

        department.study_resource.add(study_resource)
        department.study_resource.remove(study_resource)

        updated_department = Department.objects.get(pk=department.pk)
        self.assertEqual(updated_department.study_resource.count(), 0)
        self.assertFalse(
            updated_department.study_resource.filter(pk=department.pk).exists()
        )


class AttendanceTestCase(TestCase):
    fixtures = [
        "data/test_fixtures/AttendanceTestCase.json",
        "data/test_fixtures/SubjectTestCase.json",
        "data/test_fixtures/WeightageTestCase.json",
    ]

    def test_create_attendance(self):
        subject = Subject.objects.get(subject_short_name="FCSP-2")
        attendance = Attendance.objects.create(
            date="2023-07-26",
            subject=subject,
            lecture_no="3",
            mode="R",
            present=True,
        )

        self.assertEqual(Attendance.objects.count(), 3)
        self.assertTrue(
            Attendance.objects.filter(
                date="2023-07-26",
                subject=subject,
                lecture_no="3",
                mode="R",
                present=True,
            ).exists()
        )

    def test_read_attendance(self):
        attendance = Attendance.objects.get(date="2023-07-24")
        self.assertEqual(attendance.subject.subject_short_name, "FCSP-2")

    def test_update_attendance(self):
        attendance = Attendance.objects.get(date="2023-07-24")

        attendance.mode = "PRX"
        attendance.save()

        updated_attendance = Attendance.objects.get(pk=attendance.pk)

        self.assertEqual(updated_attendance.mode, "PRX")

    def test_delete_attendance(self):
        attendance = Attendance.objects.get(date="2023-07-24")

        attendance.delete()

        self.assertEqual(Attendance.objects.count(), 1)
        self.assertFalse(Attendance.objects.filter(date="2023-07-24").exists())


class RemedialTestResultTestCase(TestCase):
    fixtures = ["data/test_fixtures/RemedialTestResultTestCase.json"]

    def test_create_remedial_test_result(self):
        remedial_test_result = RemedialTestResult.objects.create(
            theory=40.0,
            individual_project=None,
            group_project=None,
            ipe=None,
            other=None,
        )

        self.assertEqual(RemedialTestResult.objects.count(), 2)
        self.assertTrue(
            RemedialTestResult.objects.filter(id=remedial_test_result.id).exists()
        )

    def test_read_remedial_test_result(self):
        remedial_test_result = RemedialTestResult.objects.get(pk=1)
        self.assertEqual(remedial_test_result.theory, 36.0)

    def test_update_remedial_test_result(self):
        remedial_test_result = RemedialTestResult.objects.get(pk=1)

        remedial_test_result.theory = 40.0
        remedial_test_result.save()

        updated_remedial_test_result = RemedialTestResult.objects.get(
            pk=remedial_test_result.pk
        )

        self.assertEqual(updated_remedial_test_result.theory, 40.0)

    def test_delete_remedial_test_result(self):
        remedial_test_result = RemedialTestResult.objects.get(pk=1)

        remedial_test_result.delete()

        self.assertEqual(RemedialTestResult.objects.count(), 0)
        self.assertFalse(RemedialTestResult.objects.filter(pk=1).exists())


class TestResultTestCase(TestCase):
    fixtures = [
        "data/test_fixtures/TestResultTestCase.json",
        "data/test_fixtures/RemedialTestResultTestCase.json",
        "data/test_fixtures/SubjectTestCase.json"
        # "data/test_fixtures/WeightageTestCase.json"
    ]

    def test_create_test_result(self):
        test_result = TestResult.objects.create(
            subject_id="12546525",
            t1=12.0,
            t2=12.0,
            t3=9.0,
            t4=10.0,
            t1_file="",
            t2_file="",
            t3_file="",
            t4_file="",
            individual_project=None,
            group_project=None,
            ipe=None,
            other=None,
            bonus=None,
        )

        self.assertEqual(TestResult.objects.count(), 3)
        self.assertTrue(TestResult.objects.filter(id=test_result.id).exists())

    def test_read_test_result(self):
        test_result = TestResult.objects.get(pk=1)
        self.assertEqual(test_result.t1, 12.0)

    def test_update_test_result(self):
        test_result = TestResult.objects.get(pk=1)

        test_result.t1 = 15.0
        test_result.save()

        updated_test_result = TestResult.objects.get(pk=test_result.pk)

        self.assertEqual(updated_test_result.t1, 15.0)

    def test_delete_test_result(self):
        test_result = TestResult.objects.get(pk=1)

        test_result.delete()

        self.assertEqual(TestResult.objects.count(), 1)
        self.assertFalse(TestResult.objects.filter(pk=1).exists())

    def test_add_remedial_to_test(self):
        test_result = TestResult.objects.create(
            subject_id="12546525",
            t1=10.0,
            t2=14.0,
            t3=8.0,
            t4=12.0,
            t1_file="",
            t2_file="",
            t3_file="",
            t4_file="",
            individual_project=None,
            group_project=None,
            ipe=None,
            other=None,
            bonus=None,
        )
        remedial_test_result = RemedialTestResult.objects.create(
            theory=40.0,
            individual_project=None,
            group_project=None,
            ipe=None,
            other=None,
        )

        test_result.remedial_result.add(remedial_test_result)

        updated_test_result = TestResult.objects.get(pk=test_result.pk)

        self.assertEqual(updated_test_result.remedial_result.count(), 1)
        self.assertTrue(
            updated_test_result.remedial_result.filter(
                pk=remedial_test_result.pk
            ).exists()
        )

    def test_update_remedial_test_result(self):
        test_result = TestResult.objects.get(pk=1)
        existing_remedial_test_result = test_result.remedial_result.first()

        existing_remedial_test_result.theory = 45.0
        existing_remedial_test_result.individual_project = None
        existing_remedial_test_result.group_project = None
        existing_remedial_test_result.ipe = None
        existing_remedial_test_result.other = None
        existing_remedial_test_result.save()

        updated_remedial_test_result = RemedialTestResult.objects.get(
            pk=existing_remedial_test_result.pk
        )

        self.assertEqual(updated_remedial_test_result.theory, 45.0)
        self.assertIsNone(updated_remedial_test_result.individual_project)
        self.assertIsNone(updated_remedial_test_result.group_project)
        self.assertIsNone(updated_remedial_test_result.ipe)
        self.assertIsNone(updated_remedial_test_result.other)

    def test_remove_remedial_from_test(self):
        test_result = TestResult.objects.get(pk=1)
        remedial_test_result = RemedialTestResult.objects.get(pk=1)

        test_result.remedial_result.remove(remedial_test_result)

        updated_test_result = TestResult.objects.get(pk=test_result.pk)

        self.assertEqual(updated_test_result.remedial_result.count(), 0)
        self.assertFalse(
            updated_test_result.remedial_result.filter(
                pk=remedial_test_result.pk
            ).exists()
        )


class MOOCCourseTestCase(TestCase):
    fixtures = ["data/test_fixtures/MOOCCourseTestCase.json"]

    def test_create_mooc_course(self):
        mooc_course = MOOCCourse.objects.create(
            course_name="Course 2",
            platform="Platform 2",
            university="University 2",
        )

        self.assertEqual(MOOCCourse.objects.count(), 2)
        self.assertTrue(MOOCCourse.objects.filter(id=mooc_course.id).exists())

    def test_read_mooc_course(self):
        mooc_course = MOOCCourse.objects.get(pk=1)
        self.assertEqual(mooc_course.course_name, "MOOC Course1")

    def test_update_mooc_course(self):
        mooc_course = MOOCCourse.objects.get(pk=1)

        mooc_course.course_name = "Updated Course1"
        mooc_course.save()

        updated_mooc_course = MOOCCourse.objects.get(pk=mooc_course.pk)

        self.assertEqual(updated_mooc_course.course_name, "Updated Course1")

    def test_delete_mooc_course(self):
        mooc_course = MOOCCourse.objects.get(pk=1)

        mooc_course.delete()

        self.assertEqual(MOOCCourse.objects.count(), 0)
        self.assertFalse(MOOCCourse.objects.filter(pk=1).exists())


class MOOCResultTestCase(TestCase):
    fixtures = [
        "data/test_fixtures/MOOCResultTestCase.json",
        "data/test_fixtures/MOOCCourseTestCase.json",
    ]

    def test_create_mooc_result(self):
        mooc_course = MOOCCourse.objects.create(
            course_name="Course B",
            platform="Platform B",
            university="University B",
        )

        mooc_result = MOOCResult.objects.create(
            course=mooc_course,
            percentage=85.0,
            certificate="https://example.com/certificate",
        )

        self.assertEqual(MOOCResult.objects.count(), 2)
        self.assertTrue(MOOCResult.objects.filter(id=mooc_result.id).exists())

    def test_read_mooc_result(self):
        mooc_result = MOOCResult.objects.get(pk=1)
        self.assertEqual(mooc_result.percentage, 80.0)

    def test_update_mooc_result(self):
        mooc_result = MOOCResult.objects.get(pk=1)

        mooc_result.percentage = 90.0
        mooc_result.save()

        updated_mooc_result = MOOCResult.objects.get(pk=mooc_result.pk)

        self.assertEqual(updated_mooc_result.percentage, 90.0)

    def test_delete_mooc_result(self):
        mooc_result = MOOCResult.objects.get(pk=1)

        mooc_result.delete()

        self.assertEqual(MOOCResult.objects.count(), 0)
        self.assertFalse(MOOCResult.objects.filter(pk=1).exists())


class IndividualProjectTestCase(TestCase):
    fixtures = [
        "data/test_fixtures/IndividualProjectTestCase.json",
        "data/test_fixtures/SubjectTestCase.json",
        "data/test_fixtures/WeightageTestCase.json",
    ]

    def test_create_individual_project(self):
        subject = Subject.objects.get(subject_short_name="FSD-2")

        individual_project = IndividualProject.objects.create(
            subject=subject,
            definition="This is the definition of the individual project.",
        )

        self.assertEqual(IndividualProject.objects.count(), 3)
        self.assertTrue(
            IndividualProject.objects.filter(id=individual_project.id).exists()
        )

    def test_read_individual_project(self):
        individual_project = IndividualProject.objects.get(pk=1)
        self.assertEqual(individual_project.subject.subject_short_name, "FCSP-2")

    def test_update_individual_project(self):
        individual_project = IndividualProject.objects.get(pk=1)

        individual_project.definition = "Updated definition of individual project."
        individual_project.save()

        updated_individual_project = IndividualProject.objects.get(
            pk=individual_project.pk
        )

        self.assertEqual(
            updated_individual_project.definition,
            "Updated definition of individual project.",
        )

    def test_delete_individual_project(self):
        individual_project = IndividualProject.objects.get(pk=1)

        individual_project.delete()

        self.assertEqual(IndividualProject.objects.count(), 1)
        self.assertFalse(IndividualProject.objects.filter(pk=1).exists())


class GroupProjectTestCase(TestCase):
    fixtures = [
        "data/test_fixtures/GroupProjectTestCase.json",
        "data/test_fixtures/SubjectTestCase.json",
        "data/test_fixtures/WeightageTestCase.json",
    ]

    def test_create_group_project(self):
        subject = subject = Subject.objects.get(subject_short_name="FSD-2")

        group_project = GroupProject.objects.create(
            subject=subject,
            definition="This is the definition of the group project.",
        )

        self.assertEqual(GroupProject.objects.count(), 2)
        self.assertTrue(GroupProject.objects.filter(id=group_project.id).exists())

    def test_read_group_project(self):
        group_project = GroupProject.objects.get(pk=1)
        self.assertEqual(group_project.subject.subject_short_name, "FCSP-2")

    def test_update_group_project(self):
        group_project = GroupProject.objects.get(pk=1)

        group_project.definition = "Updated definition of group project."
        group_project.save()

        updated_group_project = GroupProject.objects.get(pk=group_project.pk)

        self.assertEqual(
            updated_group_project.definition,
            "Updated definition of group project.",
        )

    def test_delete_group_project(self):
        group_project = GroupProject.objects.get(pk=1)

        group_project.delete()

        self.assertEqual(GroupProject.objects.count(), 0)
        self.assertFalse(GroupProject.objects.filter(pk=1).exists())


class StudentSemesterRecordTestCase(TestCase):
    fixtures = [
        "data/test_fixtures/StudentSemesterRecordTestCase.json",
        "data/test_fixtures/StudentDetailTestCase.json",
        "data/test_fixtures/DepartmentTestCase.json",
        "data/test_fixtures/AttendanceTestCase.json",
        "data/test_fixtures/TestResultTestCase.json",
        "data/test_fixtures/MOOCResultTestCase.json",
        "data/test_fixtures/MOOCCourseTestCase.json",
        "data/test_fixtures/IndividualProjectTestCase.json",
        "data/test_fixtures/GroupProjectTestCase.json",
        "data/test_fixtures/BranchTestCase.json",
        "data/test_fixtures/StaffDetailTestCase.json",
        "data/test_fixtures/BatchTestCase.json",
        "data/test_fixtures/SubjectTestCase.json",
        "data/test_fixtures/WeightageTestCase.json",
        "data/test_fixtures/FacultyAllocationTestCase.json",
        "data/test_fixtures/RemedialTestResultTestCase.json",
    ]

    def test_create_student_semester_record(self):
        student = StudentDetail.objects.get(email="student3@ljku.edu.in")
        department = Department.objects.get(pk=1)

        student_semester_record = StudentSemesterRecord.objects.create(
            student=student,
            department=department,
            roll_no=15,
        )

        self.assertEqual(StudentSemesterRecord.objects.count(), 3)
        self.assertTrue(
            StudentSemesterRecord.objects.filter(id=student_semester_record.id).exists()
        )

    def test_read_student_semester_record(self):
        student_semester_record = StudentSemesterRecord.objects.get(pk=1)
        self.assertEqual(student_semester_record.roll_no, 14)

    def test_update_student_semester_record(self):
        student_semester_record = StudentSemesterRecord.objects.get(pk=1)

        student_semester_record.roll_no = 20
        student_semester_record.save()

        updated_student_semester_record = StudentSemesterRecord.objects.get(
            pk=student_semester_record.pk
        )

        self.assertEqual(updated_student_semester_record.roll_no, 20)

    def test_delete_student_semester_record(self):
        student_semester_record = StudentSemesterRecord.objects.get(pk=1)

        student_semester_record.delete()

        self.assertEqual(StudentSemesterRecord.objects.count(), 1)
        self.assertFalse(StudentSemesterRecord.objects.filter(pk=1).exists())

    def test_add_attendance_to_studentrecord(self):
        subject = Subject.objects.get(subject_short_name="FSD-2")
        attendance = Attendance.objects.create(
            date="2023-07-26",
            subject=subject,
            lecture_no="3",
            mode="R",
            present=True,
        )

        student = StudentDetail.objects.get(email="student3@ljku.edu.in")
        department = Department.objects.get(pk=1)

        student_semester_record = StudentSemesterRecord.objects.create(
            student=student,
            department=department,
            roll_no=21,
        )

        student_semester_record.attendance.add(attendance)

        updated_student_semester_record = StudentSemesterRecord.objects.get(
            pk=student_semester_record.pk
        )

        self.assertEqual(updated_student_semester_record.attendance.count(), 1)
        self.assertTrue(
            updated_student_semester_record.attendance.filter(
                pk=student_semester_record.pk
            ).exists()
        )

    def test_update_attendance_to_studentrecord(self):
        student_semester_record = StudentSemesterRecord.objects.get(pk=1)
        existing_attendance = student_semester_record.attendance.get(pk=2)
        existing_attendance.mode = "PRX"
        existing_attendance.present = True
        existing_attendance.save()

        updated_student_semester_record = StudentSemesterRecord.objects.get(
            pk=student_semester_record.pk
        )

        self.assertEqual(
            existing_attendance.mode,
            updated_student_semester_record.attendance.get(pk=2).mode,
        )

    def test_remove_attendance_to_studentrecord(self):
        student_semester_record = StudentSemesterRecord.objects.get(pk=1)
        attendance = Attendance.objects.get(pk=2)

        student_semester_record.attendance.remove(attendance)

        updated_student_semester_record = StudentSemesterRecord.objects.get(
            pk=student_semester_record.pk
        )

        self.assertEqual(updated_student_semester_record.attendance.count(), 0)
        self.assertFalse(
            updated_student_semester_record.attendance.filter(
                pk=student_semester_record.pk
            ).exists()
        )

    def test_add_testresult_to_studentrecord(self):
        subject = Subject.objects.get(subject_short_name="FSD-2")
        test_result = TestResult.objects.create(
            subject_id="12546525",
            t1=12.0,
            t2=12.0,
            t3=9.0,
            t4=10.0,
            t1_file="",
            t2_file="",
            t3_file="",
            t4_file="",
            individual_project=None,
            group_project=None,
            ipe=None,
            other=None,
            bonus=None,
        )
        student = StudentDetail.objects.get(email="student3@ljku.edu.in")
        department = Department.objects.get(pk=1)

        student_semester_record = StudentSemesterRecord.objects.create(
            student=student,
            department=department,
            roll_no=21,
        )

        student_semester_record.test_result.add(test_result)

        updated_student_semester_record = StudentSemesterRecord.objects.get(
            pk=student_semester_record.pk
        )

        self.assertEqual(updated_student_semester_record.test_result.count(), 1)
        self.assertTrue(
            updated_student_semester_record.test_result.filter(
                pk=test_result.pk
            ).exists()
        )

    def test_update_testresult_to_studentrecord(self):
        student_semester_record = StudentSemesterRecord.objects.get(pk=1)
        existing_test_result = student_semester_record.test_result.get(pk=1)
        existing_test_result.t1 = 25.0
        existing_test_result.save()

        updated_student_semester_record = StudentSemesterRecord.objects.get(
            pk=student_semester_record.pk
        )

        self.assertEqual(
            existing_test_result.t1,
            updated_student_semester_record.test_result.get(pk=1).t1,
        )

    def test_remove_testresult_to_studentrecord(self):
        student_semester_record = StudentSemesterRecord.objects.get(pk=1)
        test_result = TestResult.objects.get(pk=1)

        student_semester_record.test_result.remove(test_result)

        updated_student_semester_record = StudentSemesterRecord.objects.get(
            pk=student_semester_record.pk
        )

        self.assertEqual(updated_student_semester_record.test_result.count(), 0)
        self.assertFalse(
            updated_student_semester_record.test_result.filter(
                pk=student_semester_record.pk
            ).exists()
        )

    def test_add_mooccourse_to_studentrecord(self):
        student_semester_record = StudentSemesterRecord.objects.get(pk=2)

        mooc_course = MOOCCourse.objects.create(
            course_name="Course B",
            platform="Platform B",
            university="University B",
        )

        mooc_result = MOOCResult.objects.create(
            course=mooc_course,
            percentage=85.0,
            certificate="https://example.com/certificate",
        )

        student_semester_record.mooc_course.add(mooc_result)

        updated_student_semester_record = StudentSemesterRecord.objects.get(
            pk=student_semester_record.pk
        )

        self.assertEqual(updated_student_semester_record.mooc_course.count(), 1)
        self.assertTrue(
            updated_student_semester_record.mooc_course.filter(
                pk=student_semester_record.pk
            ).exists()
        )

    def test_update_mooccourse_to_studentrecord(self):
        student_semester_record = StudentSemesterRecord.objects.get(pk=1)

        mooc_course = MOOCCourse.objects.create(
            course_name="Course A",
            platform="Platform A",
            university="University A",
        )

        mooc_result = MOOCResult.objects.create(
            course=mooc_course,
            percentage=85.0,
            certificate="https://example.com/certificate",
        )
        student_semester_record.mooc_course.clear()

        student_semester_record.mooc_course.add(mooc_result)

        student_semester_record.save()

        updated_student_semester_record = StudentSemesterRecord.objects.get(
            pk=student_semester_record.pk
        )

        self.assertIn(mooc_result, updated_student_semester_record.mooc_course.all())

        self.assertIsNotNone(updated_student_semester_record.mooc_course.first())

    def test_remove_mooccourse_to_studentrecord(self):
        student_semester_record = StudentSemesterRecord.objects.get(pk=1)
        mooc_course = MOOCResult.objects.get(pk=1)

        student_semester_record.mooc_course.remove(mooc_course)

        updated_student_semester_record = StudentSemesterRecord.objects.get(
            pk=student_semester_record.pk
        )

        self.assertEqual(updated_student_semester_record.mooc_course.count(), 0)
        self.assertFalse(
            updated_student_semester_record.mooc_course.filter(
                pk=student_semester_record.pk
            ).exists()
        )

    def test_add_individual_to_studentrecord(self):
        subject = Subject.objects.get(subject_short_name="FSD-2")

        individual_project = IndividualProject.objects.create(
            subject=subject,
            definition="This is the definition of the individual project.",
        )

        student = StudentDetail.objects.create(
            enrolment_no="25468521268",
            email="student4@ljku.edu.in",
            first_name="sfname4",
            last_name="slname4",
            gender="M",
            birth_date="2004-04-04",
            mobile_number="+1112223334",
            branch=Branch.objects.all()[0],
        )
        department = Department.objects.get(pk=1)

        student_semester_record = StudentSemesterRecord.objects.create(
            student=student,
            department=department,
            roll_no=21,
        )

        student_semester_record.individual_project.add(individual_project)

        updated_student_semester_record = StudentSemesterRecord.objects.get(
            pk=student_semester_record.pk
        )

        self.assertEqual(updated_student_semester_record.individual_project.count(), 1)
        self.assertTrue(
            updated_student_semester_record.individual_project.filter(
                pk=individual_project.pk
            ).exists()
        )

    def test_update_individual_to_studentrecord(self):
        student_semester_record = StudentSemesterRecord.objects.get(pk=1)
        individual_project = IndividualProject.objects.get(pk=1)

        student_semester_record.individual_project.clear()

        student_semester_record.individual_project.add(individual_project)

        student_semester_record.save()

        updated_student_semester_record = StudentSemesterRecord.objects.get(
            pk=student_semester_record.pk
        )

        self.assertIn(
            individual_project, updated_student_semester_record.individual_project.all()
        )

        self.assertIsNotNone(updated_student_semester_record.individual_project.first())

    def test_remove_individual_to_studentrecord(self):
        student_semester_record = StudentSemesterRecord.objects.get(pk=1)
        individual_project = IndividualProject.objects.get(pk=2)

        student_semester_record.individual_project.remove(individual_project)

        updated_student_semester_record = StudentSemesterRecord.objects.get(
            pk=student_semester_record.pk
        )

        self.assertEqual(updated_student_semester_record.individual_project.count(), 0)
        self.assertFalse(
            updated_student_semester_record.individual_project.filter(
                pk=student_semester_record.pk
            ).exists()
        )

    def test_add_group_to_studentrecord(self):
        subject = Subject.objects.get(subject_short_name="FCSP-2")

        group_project = GroupProject.objects.create(
            subject=subject,
            definition="This is the definition of the Group project.",
        )

        student = StudentDetail.objects.get(email="student3@ljku.edu.in")
        department = Department.objects.get(pk=1)

        student_semester_record = StudentSemesterRecord.objects.create(
            student=student,
            department=department,
            roll_no=20,
        )

        student_semester_record.group_project.add(group_project)

        updated_student_semester_record = StudentSemesterRecord.objects.get(
            pk=student_semester_record.pk
        )

        self.assertEqual(updated_student_semester_record.group_project.count(), 1)
        self.assertTrue(
            updated_student_semester_record.group_project.filter(
                pk=group_project.pk
            ).exists()
        )

    def test_update_group_to_studentrecord(self):
        subject = Subject.objects.get(subject_short_name="FCSP-2")
        student_semester_record = StudentSemesterRecord.objects.get(pk=1)
        group_project = GroupProject.objects.create(
            subject=subject,
            definition="This is the definition of the Group project.",
        )
        student_semester_record.group_project.clear()

        student_semester_record.group_project.add(group_project)

        student_semester_record.save()

        updated_student_semester_record = StudentSemesterRecord.objects.get(
            pk=student_semester_record.pk
        )

        self.assertIn(
            group_project, updated_student_semester_record.group_project.all()
        )

        self.assertIsNotNone(updated_student_semester_record.group_project.first())

    def test_remove_group_to_studentrecord(self):
        student_semester_record = StudentSemesterRecord.objects.get(pk=1)
        group_project = GroupProject.objects.get(pk=1)

        student_semester_record.group_project.remove(group_project)

        updated_student_semester_record = StudentSemesterRecord.objects.get(
            pk=student_semester_record.pk
        )

        self.assertEqual(updated_student_semester_record.group_project.count(), 0)
        self.assertFalse(
            updated_student_semester_record.group_project.filter(
                pk=student_semester_record.pk
            ).exists()
        )
