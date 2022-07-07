from django.contrib import admin
from . import models

admin.site.register(models.Gallery)
admin.site.register(models.Image)
admin.site.register(models.Category)
admin.site.register(models.Food)
admin.site.register(models.Drink)
admin.site.register(models.MealGroup)
admin.site.register(models.Discount)

