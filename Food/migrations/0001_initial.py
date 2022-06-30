# Generated by Django 3.2 on 2022-06-30 14:36

import Food.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField(default=0)),
                ('status_show', models.CharField(choices=[('show', 'Show'), ('hide', 'Hide')], default='show', max_length=10)),
                ('type_of_time_serve', models.CharField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner')], max_length=10)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Food.category')),
                ('gallery', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Food.gallery')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('meal_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Food.meal')),
                ('type_meal', models.CharField(default='drink', editable=False, max_length=10)),
            ],
            options={
                'abstract': False,
            },
            bases=('Food.meal',),
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('meal_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Food.meal')),
                ('type_meal', models.CharField(default='food', editable=False, max_length=10)),
            ],
            options={
                'abstract': False,
            },
            bases=('Food.meal',),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=Food.models.upload_image_gallery_src)),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Food.gallery')),
            ],
        ),
        migrations.CreateModel(
            name='MealGroup',
            fields=[
                ('meal_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Food.meal')),
                ('type_meal', models.CharField(default='group', editable=False, max_length=10)),
                ('use_discounts_meal', models.BooleanField(default=True)),
                ('drinks', models.ManyToManyField(to='Food.Drink')),
                ('foods', models.ManyToManyField(to='Food.Food')),
            ],
            options={
                'abstract': False,
            },
            bases=('Food.meal',),
        ),
    ]
