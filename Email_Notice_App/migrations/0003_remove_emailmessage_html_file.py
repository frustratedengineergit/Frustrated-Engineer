# Generated by Django 4.1.3 on 2023-05-31 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Email_Notice_App", "0002_emailmessage_html_file"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="emailmessage",
            name="html_file",
        ),
    ]
