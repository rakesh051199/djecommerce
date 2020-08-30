# Generated by Django 3.0.8 on 2020-08-02 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200801_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('ow', 'outwear'), ('sw', 'sportswear'), ('s', 'shirt')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('s', 'secondary'), ('r', 'danger'), ('p', 'primary')], max_length=1),
        ),
    ]
