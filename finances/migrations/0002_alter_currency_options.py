# Generated by Django 4.2.1 on 2023-07-30 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currency',
            options={'verbose_name_plural': 'currencies'},
        ),
    ]
