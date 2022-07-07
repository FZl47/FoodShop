from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Discount
from django_q.models import Schedule


name_task_delete_discount = 'Task_Delete_Discount_{}'

@receiver(post_save,sender=Discount)
def create_task_schedule_discount(sender,instance,created,**kwargs):
    if created:
        Schedule.objects.create(
            name=name_task_delete_discount.format(instance.id),
            func='Food.tasks.delete_discount',
            args=f'{instance.id},',
            repeats=1,
            next_run=instance.time_end
        )


@receiver(post_delete,sender=Discount)
def delete_task_schedule_discount(sender,instance,**kwargs):
    try:
        task = Schedule.objects.get(name=name_task_delete_discount.format(instance.id))
        task.delete()
    except:
        pass