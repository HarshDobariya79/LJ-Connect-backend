import json
from copy import deepcopy

from django.core.serializers import serialize
from django.db.models.signals import (m2m_changed, post_delete, post_save,
                                      pre_delete, pre_save)
from django.dispatch import receiver

from .models import Batch, Department, FacultyAllocation
from .utils import delete_empty_keys

HOD_PERMISSIONS = {
    "attendance": {"create": True, "read": True, "update": True, "delete": True},
    "test_result": {"create": True, "read": True, "update": True, "delete": True},
    "project": {"create": True, "read": True, "update": True, "delete": True},
    "mooc": {"create": True, "read": True, "update": True, "delete": True},
}

FACULTY_PERMISSIONS = {
    "attendance": {"create": True, "read": True, "update": False, "delete": False},
    "test_result": {"create": True, "read": True, "update": False, "delete": False},
    "project": {"create": True, "read": True, "update": True, "delete": False},
    "mooc": {"create": True, "read": True, "update": False, "delete": False},
}


# Department model signals


@receiver(pre_save, sender=Department)
@receiver(m2m_changed, sender=Department.batch.through)
def handle_department_modifications(
    sender, instance, action=None, reverse=None, model=None, pk_set=None, **kwargs
):
    try:
        if (
            action == "pre_add" or action == None
        ):  # handle adding new batches to a department (department creation will also trigger this)
            if action == "pre_add":
                updated_batch_list = Batch.objects.filter(pk__in=pk_set)
            else:
                original_department = Department.objects.get(pk=instance.pk)
                updated_batch_list = original_department.batch.all()
            hod = instance.hod

            permissions_format = {
                instance.year: {instance.semester: {instance.name: {}}}
            }

            hod_permissions = deepcopy(permissions_format)
            hod_permissions.update(hod.permissions)

            for batch in updated_batch_list:
                hod_permissions[instance.year][instance.semester][instance.name][
                    batch.name
                ] = deepcopy(HOD_PERMISSIONS)
                for staff in batch.faculty.all():
                    if staff.faculty.email == instance.hod.email:
                        continue
                    faculty_permissions = deepcopy(permissions_format)
                    faculty_permissions.update(staff.faculty.permissions)
                    faculty_permissions[instance.year][instance.semester][
                        instance.name
                    ][batch.name] = deepcopy(FACULTY_PERMISSIONS)
                    staff.faculty.permissions.update(faculty_permissions)
                    staff.faculty.save()
            hod.permissions.update(hod_permissions)
            delete_empty_keys(hod.permissions)
            hod.save()

        elif action == "pre_remove":  # handle removing batches from a department
            removed_batches = Batch.objects.filter(pk__in=pk_set)
            hod = instance.hod
            department = hod.permissions[instance.year][instance.semester][
                instance.name
            ]

            for batch, _ in department.items():
                for batch in removed_batches:
                    department[batch.name] = {}
            delete_empty_keys(hod.permissions)
            hod.save()

            for batch in removed_batches:
                for staff in batch.faculty.all():
                    if instance.hod.email == staff.faculty.email:
                        continue
                    staff.faculty.permissions[instance.year][instance.semester][
                        instance.name
                    ][batch.name] = {}
                    delete_empty_keys(staff.faculty.permissions)
                    staff.faculty.save()
                batch.delete()

        if action == None:  # handle changing HOD of a department
            if instance.pk:
                original_department = Department.objects.get(pk=instance.pk)
                old_hod_permissions = original_department.hod.permissions

                for batch in original_department.batch.all():
                    isHod = False
                    for staff in batch.faculty.all():
                        if staff.faculty.email == original_department.hod.email:
                            isHod = True
                    if isHod:
                        old_hod_permissions[instance.year][instance.semester][
                            instance.name
                        ][batch.name] = FACULTY_PERMISSIONS
                    else:
                        del old_hod_permissions[instance.year][instance.semester][
                            instance.name
                        ][batch.name]
                delete_empty_keys(original_department.hod.permissions)
                original_department.hod.save()

    except Exception as e:
        print(action, "WARNING", e)


@receiver(pre_delete, sender=Department)
def handle_hod_updation(sender, instance, **kwargs):  # handle deleting a department
    try:
        if instance.pk:
            original_department = Department.objects.get(pk=instance.pk)
            old_hod_permissions = original_department.hod.permissions
            del original_department.hod.permissions[instance.year][instance.semester][
                instance.name
            ]

            for batch in original_department.batch.all():
                for staff in batch.faculty.all():
                    del staff.faculty.permissions[instance.year][instance.semester][
                        instance.name
                    ][batch.name]
                    delete_empty_keys(staff.faculty.permissions)
                    staff.faculty.save()
                batch.delete()
            delete_empty_keys(original_department.hod.permissions)
            original_department.hod.save()
    except Exception as e:
        print("WARNING", e)


# Batch model signals


@receiver(m2m_changed, sender=Batch.faculty.through)
def handle_batch_faculty_updation(
    sender, instance, action=None, reverse=None, model=None, pk_set=None, **kwargs
):
    try:
        if action == "pre_add":  # handle adding new faculty to a batch
            added_faculties = FacultyAllocation.objects.filter(pk__in=pk_set)

            batch = instance

            for department in instance.department_set.all():
                hod = department.hod

                permissions_format = {
                    department.year: {department.semester: {department.name: {}}}
                }

                hod_permissions = deepcopy(permissions_format)
                hod_permissions.update(hod.permissions)
                hod_permissions[department.year][department.semester][department.name][
                    batch.name
                ] = deepcopy(HOD_PERMISSIONS)
                hod.permissions.update(hod_permissions)
                delete_empty_keys(hod.permissions)
                hod.save()

                for staff in added_faculties:
                    if staff.faculty.email == hod.email:
                        continue
                    faculty_permissions = deepcopy(permissions_format)
                    faculty_permissions.update(staff.faculty.permissions)
                    faculty_permissions[department.year][department.semester][
                        department.name
                    ][batch.name] = deepcopy(FACULTY_PERMISSIONS)
                    staff.faculty.permissions.update(faculty_permissions)
                    staff.faculty.save()

        elif action == "pre_remove":  # handle removing faculties from a batch
            removed_faculties = FacultyAllocation.objects.filter(pk__in=pk_set)

            for department in instance.department_set.all():
                hod = department.hod
                batch = instance

                for staff in removed_faculties:
                    if hod.email == staff.faculty.email:
                        continue
                    staff.faculty.permissions[department.year][department.semester][
                        department.name
                    ][batch.name] = {}
                    delete_empty_keys(staff.faculty.permissions)
                    staff.faculty.save()

    except Exception as e:
        print(action, "WARNING", e)


@receiver(pre_delete, sender=Batch)
def handle_batch_delete(sender, instance, **kwargs):
    try:
        if instance.pk:
            batch = Batch.objects.get(pk=instance.pk)
            departments = batch.department_set.all()

            for department in departments:
                del department.hod.permissions[department.year][department.semester][
                    department.name
                ][batch.name]
                delete_empty_keys(department.hod.permissions)
                department.hod.save()
                for staff in batch.faculty.all():
                    del staff.faculty.permissions[department.year][department.semester][
                        department.name
                    ][batch.name]
                    delete_empty_keys(staff.faculty.permissions)
                    staff.faculty.save()

    except Exception as e:
        print("WARNING", e)
