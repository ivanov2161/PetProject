# Generated by Django 4.1.3 on 2022-12-08 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goen', '0002_book_cover'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Book',
            new_name='Story',
        ),
        migrations.AlterModelTable(
            name='story',
            table='stories',
        ),
    ]
