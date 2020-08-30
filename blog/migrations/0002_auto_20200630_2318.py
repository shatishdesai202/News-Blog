# Generated by Django 3.0.5 on 2020-06-30 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ManyToManyField(blank=True, null=True, to='blog.Author'),
        ),
    ]