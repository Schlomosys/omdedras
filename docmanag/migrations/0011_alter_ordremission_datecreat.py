# Generated by Django 3.2.5 on 2021-10-17 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docmanag', '0010_auto_20211017_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordremission',
            name='datecreat',
            field=models.DateField(blank=True, null=True),
        ),
    ]
