# Generated by Django 3.0.8 on 2020-08-02 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200802_1040'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='item',
            new_name='Item',
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('sw', 'sportswear'), ('s', 'shirt'), ('ow', 'outwear')], max_length=2),
        ),
    ]