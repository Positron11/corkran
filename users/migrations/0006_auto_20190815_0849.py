# Generated by Django 2.2.4 on 2019-08-15 08:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0005_sitesettings'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SiteSettings',
            new_name='Setting',
        ),
    ]