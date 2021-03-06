# Generated by Django 3.0.8 on 2020-08-22 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_auto_20200821_1151'),
    ]

    operations = [
        migrations.DeleteModel(
            name='carousel',
        ),
        migrations.AddField(
            model_name='item',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('S', 'shipping'), ('B', 'billing')], max_length=1),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('s', 'shirt'), ('ow', 'outwear'), ('sw', 'sportswear')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('p', 'primary'), ('r', 'danger'), ('s', 'secondary')], max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Payment'),
        ),
    ]
