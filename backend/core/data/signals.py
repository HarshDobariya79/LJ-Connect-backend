import json
from copy import deepcopy

from django.core.serializers import serialize
from django.db.models.signals import (m2m_changed, post_delete, post_save,
                                      pre_delete, pre_save)
from django.dispatch import receiver

from .models import Batch, Department, FacultyAllocation
from .utils import delete_empty_keys, permissions_assign

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


def permission_assignment_from_batches(instance, batches):
    try:
        hod = instance.hod
        for batch in batches:
            permissions_assign(
                hod.permissions,
                [instance.year, instance.semester, instance.name, batch.name],
                HOD_PERMISSIONS,
            )
            for staff in batch.faculty.all():
                if staff.faculty.email == hod.email:
                    continue
                permissions_assign(
                    staff.faculty.permissions,
                    [instance.year, instance.semester, instance.name, batch.name],
                    FACULTY_PERMISSIONS,
                )
                staff.faculty.save()
        hod.save()
    except Exception as e:
        pass
        # print(f"permission assignment from batches {e}")


def permission_assignment_from_department(instance):
    try:
        batches = instance.batch.all()
        permission_assignment_from_batches(instance, batches)
    except Exception as e:
        pass
        # print(f"permission assignment from department {e}")


def permission_revocation_from_batches(instance, batches):
    try:
        hod = instance.hod

        for batch in batches:
            del hod.permissions[instance.year][instance.semester][instance.name][
                batch.name
            ]
            delete_empty_keys(hod.permissions)
        hod.save()

        for batch in batches:
            for staff in batch.faculty.all():
                if staff.faculty.email == hod.email:
                    continue
                del staff.faculty.permissions[instance.year][instance.semester][
                    instance.name
                ][batch.name]
                delete_empty_keys(staff.faculty.permissions)
                staff.faculty.save()
    except Exception as e:
        pass
        # print(f"permission revocation from batches {e}")


def permission_revocation_from_department(instance):
    try:
        hod = instance.hod
        del hod.permissions[instance.year][instance.semester][instance.name]
        delete_empty_keys(hod.permissions)
        hod.save()

        for batch in instance.batch.all():
            for staff in batch.faculty.all():
                try:
                    del staff.faculty.permissions[instance.year][instance.semester][
                        instance.name
                    ]
                except Exception as e:
                    pass
                delete_empty_keys(staff.faculty.permissions)
                staff.faculty.save()

    except Exception as e:
        pass
        # print(f"permission revocation from department {e}")


def hod_permission_transfer(instance):
    try:
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
        pass
        # print(f"hod permission transfer {e}")


@receiver(m2m_changed, sender=Department.batch.through)
def m2m_changed_handler(sender, instance, action, reverse, model, pk_set, **kwargs):
    try:
        if action == "post_add":
            batches = Batch.objects.filter(pk__in=pk_set)
            permission_assignment_from_batches(instance, batches)

        elif action == "post_remove":
            batches = Batch.objects.filter(pk__in=pk_set)
            permission_revocation_from_batches(instance, batches)
            for batch in batches:
                batch.delete()
    except Exception as e:
        pass
        # print(f"m2m change department batch {e}")


@receiver(pre_save, sender=Department)
def handle_department_modifications(
    sender, instance, **kwargs
):  # It'll also handle department creation
    try:
        if instance.pk:
            old_instance = sender.objects.get(pk=instance.pk)
            if old_instance.locked and not instance.locked:
                permission_assignment_from_department(instance)
            elif not old_instance.locked and instance.locked:
                permission_revocation_from_department(instance)
            elif not old_instance.locked and not instance.locked:
                if old_instance.hod.email != instance.hod.email:
                    hod_permission_transfer(instance)
                    permission_assignment_from_department(instance)

    except Exception as e:
        pass
        # print(f"department pre_save {e}")


@receiver(pre_delete, sender=Department)
def handle_hod_updation(sender, instance, **kwargs):  # handle deleting a department
    try:
        if instance.pk:
            permission_revocation_from_department(instance)
            for batch in instance.batch.all():
                batch.delete()
    except Exception as e:
        pass
        # print("WARNING", e)


# Batch signals


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
                permissions_assign(
                    hod.permissions,
                    [department.year, department.semester, department.name, batch.name],
                    HOD_PERMISSIONS,
                )
                hod.save()

                for staff in added_faculties:
                    if staff.faculty.email == hod.email:
                        continue
                    permissions_assign(
                        staff.faculty.permissions,
                        [
                            department.year,
                            department.semester,
                            department.name,
                            batch.name,
                        ],
                        FACULTY_PERMISSIONS,
                    )
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
        pass
        # print(action, "WARNING", e)


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
        pass
        # print("WARNING", e)
