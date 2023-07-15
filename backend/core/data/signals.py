from django.db.models.signals import pre_save, post_save, pre_delete, post_delete, m2m_changed
from django.dispatch import receiver
from .models import Department
from django.core.serializers import serialize
import json
from .utils import delete_empty_keys

# Department model signals

@receiver(post_save, sender=Department)
@receiver(m2m_changed, sender=Department.batch.through)
def handle_department_modifications(sender, instance, action=None, **kwargs):
    
    if action == 'post_add' or action == 'post_remove' or action == None:

        hod = instance.hod

        permissions_json = {
            instance.year: {
                instance.semester: {
                    instance.name: {

                    }
                }
            }
        }

        serialized_data = json.loads(serialize('json', instance.batch.all()))
        updated_batch_list = list(map(lambda x: x["fields"]["name"], serialized_data))
        
        for batch in updated_batch_list:
            permissions_json[instance.year][instance.semester][instance.name][batch] = {
                "attendance": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True
                },
                "test_result": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True
                },
                "project": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True
                },
                "mooc": {
                    "create": True,
                    "read": True,
                    "update": True,
                    "delete": True
                }
            }

        hod.permissions.update(permissions_json)
        department = hod.permissions[instance.year][instance.semester][instance.name]

        if action == 'post_remove':
            for batch, _ in department.items():
                if(batch not in updated_batch_list):
                    del department[batch]
        delete_empty_keys(hod.permissions)

        hod.save()

@receiver(pre_save, sender=Department)
@receiver(pre_delete, sender=Department)
def handle_hod_updation(sender, instance, **kwargs):
    
    if instance.pk:

        try:
            original_department = Department.objects.get(pk=instance.pk)
            old_hod_permissions = original_department.hod.permissions

            del original_department.hod.permissions[instance.year][str(instance.semester)][instance.name]
            
            delete_empty_keys(original_department.hod.permissions)
            
            original_department.hod.save()
        except Exception as e:
            print(e)
