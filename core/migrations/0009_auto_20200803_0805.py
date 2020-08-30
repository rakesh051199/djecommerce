# Generated by Django 3.0.8 on 2020-08-03 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200802_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('ow', 'outwear'), ('sw', 'sportswear'), ('s', 'shirt')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('r', 'danger'), ('s', 'secondary'), ('p', 'primary')], max_length=1),
        ),
    ]