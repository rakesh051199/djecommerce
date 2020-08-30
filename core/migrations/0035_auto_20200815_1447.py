# Generated by Django 3.0.8 on 2020-08-15 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20200815_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='use_default',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('B', 'billing'), ('S', 'shipping')], max_length=1),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('ow', 'outwear'), ('sw', 'sportswear'), ('s', 'shirt')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('r', 'danger'), ('p', 'primary'), ('s', 'secondary')], max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Payment'),
        ),
    ]
