# Generated by Django 3.0.8 on 2020-08-03 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20200803_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('s', 'shirt'), ('sw', 'sportswear'), ('ow', 'outwear')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('r', 'danger'), ('p', 'primary'), ('s', 'secondary')], max_length=1),
        ),
    ]
