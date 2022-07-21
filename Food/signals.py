from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from .models import Meal, Discount, NotifyMe, Drink, Food, MealGroup
from django_q.models import Schedule

# Task Food
CLASS_MEALS = [Food,Drink,MealGroup]
def send_notice_available(sender,instance,**kwargs):
    """
        if instance.id is None then nothing to notify
    """
    if instance.id != None:
        available_past = sender.objects.get(id=instance.id).is_available()
        available_current = instance.is_available()
        if available_past == False and available_current == True:
            # Available
            instance.send_notify_available()
for model in CLASS_MEALS:
    pre_save.connect(send_notice_available,model)

# Task Discount
name_task_delete_discount = 'Task_Delete_Discount_{}'

@receiver(post_save, sender=Discount)
def create_task_schedule_discount(sender, instance, created, **kwargs):
    if created:
        Schedule.objects.create(
            name=name_task_delete_discount.format(instance.id),
            func='Food.tasks.delete_discount',
            args=f'{instance.id},',
            repeats=1,
            next_run=instance.time_end
        )


@receiver(post_delete, sender=Discount)
def delete_task_schedule_discount(sender, instance, **kwargs):
    try:
        task = Schedule.objects.get(name=name_task_delete_discount.format(instance.id))
        task.delete()
    except:
        pass
