import json

from django.test import TestCase

from .models import (Batch, Department, FacultyAllocation, StaffDetail,
                     StudentDetail)


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
