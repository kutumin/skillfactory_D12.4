# Generated by Django 3.2.8 on 2021-12-20 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_subscriber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscribedusers',
            name='email',
        ),
        migrations.RemoveField(
            model_name='subscribedusers',
            name='name',
        ),
        migrations.DeleteModel(
            name='Subscriber',
        ),
    ]
