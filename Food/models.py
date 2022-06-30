from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.core.validators import MaxValueValidator, MinValueValidator
from model_utils.managers import InheritanceManager
from Config import tools
import datetime


class Gallery(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        print(self.meal_set.all())
        if self.title:
            return f"Gallery - {self.title[:30]}"
        return f"Gallery"

    def get_images(self):
        return self.image_set.all()

    def get_src_directory(self):
        title = str(self.title).replace(' ', '-')
        return f"{title}-{self.id}"


def upload_image_gallery_src(instance, path):
    path = str(path).split('.')[-1]
    if path in settings.IMAGES_FORMAT:
        src = f"images/gallery/{instance.gallery.get_src_directory()}/{tools.RandomString(40)}.{path}"
        return src
    raise PermissionDenied


class Image(models.Model):
    image = models.ImageField(upload_to=upload_image_gallery_src)
    gallery = models.ForeignKey('Gallery', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image - {self.gallery.title}"


class Category(models.Model):
    title = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def title_slug(self):
        return str(self.title).replace(' ', '-')

    @property
    def slug(self):
        return str(self.title).replace(' ', '-')


class TypeTimeServeMeal(models.Model):
    title = models.CharField(max_length=50)
    start_from = models.TimeField()
    end_at = models.TimeField()

    def __str__(self):
        return self.title


class CustomManagerMeal(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(category__is_active=True, status_show='show', stock__gt=0)


class MealBase(models.Model):
    STATUS_SHOW = (
        ('show', 'Show'),
        ('hide', 'Hide')
    )

    TYPE_OF_TIME_SERVE_MEAL = (
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    gallery = models.ForeignKey('Gallery', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    stock = models.IntegerField(default=0)
    status_show = models.CharField(default='show', choices=STATUS_SHOW, max_length=10)
    type_of_time_serve = models.ManyToManyField('TypeTimeServeMeal')

    get_objects = CustomManagerMeal()

    class Meta:
        abstract = True

    def __str__(self):
        return self.title[:30]

    @property
    def title_slug(self):
        return str(self.title).replace(' ', '-')

    @property
    def slug(self):
        return str(self.title).replace(' ', '-')

    def get_images(self):
        galley = self.gallery
        if galley:
            return galley.get_images()
        return []

    def is_available_stock(self):
        return True if int(self.stock) > 0 else False

    def its_time_serve(self,time_now=None):
        if not time_now:
            time_now = tools.GetTime()
        type_of_time_serve = self.type_of_time_serve.all()

        for time_serve in type_of_time_serve:
            if tools.InBetWeenTime(time_now,time_serve.start_from,time_serve.end_at):
                return True
        return False


class Meal(MealBase):
    objects = InheritanceManager()


class Food(Meal):
    type_meal = models.CharField(default='food', editable=False, max_length=10)


class Drink(Meal):
    type_meal = models.CharField(default='drink', editable=False, max_length=10)


class MealGroup(Meal):
    """
        Group includes Food and Drink and . . . Other Meals
    """
    type_meal = models.CharField(default='group', editable=False, max_length=10)
    foods = models.ManyToManyField('Food')
    drinks = models.ManyToManyField('Drink')
    use_discounts_meal = models.BooleanField(default=True)




# class Discount(models.Model):
#     title = models.CharField(max_length=100,null=True,blank=True)
#     percentage = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
#     meals = models.ManyToManyField('Meal')




