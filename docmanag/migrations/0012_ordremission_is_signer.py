# Generated by Django 3.2.5 on 2021-10-18 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docmanag', '0011_alter_ordremission_datecreat'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordremission',
            name='is_signer',
            field=models.BooleanField(default=False),
        ),
    ]