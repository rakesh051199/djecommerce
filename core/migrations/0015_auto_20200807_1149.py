# Generated by Django 3.0.8 on 2020-08-07 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20200806_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('s', 'shirt'), ('ow', 'outwear'), ('sw', 'sportswear')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('s', 'secondary'), ('r', 'danger'), ('p', 'primary')], max_length=1),
        ),
    ]
