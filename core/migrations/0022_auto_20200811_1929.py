# Generated by Django 3.0.8 on 2020-08-11 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20200811_1158'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='srtipe_charge_id',
            new_name='stripe_charge_id',
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('ow', 'outwear'), ('s', 'shirt'), ('sw', 'sportswear')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('p', 'primary'), ('s', 'secondary'), ('r', 'danger')], max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Payment'),
        ),
    ]
