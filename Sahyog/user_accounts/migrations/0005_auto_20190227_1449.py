# Generated by Django 2.1.7 on 2019-02-27 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0004_userprofile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='prar.jpg', upload_to='profile_pics'),
        ),
    ]
