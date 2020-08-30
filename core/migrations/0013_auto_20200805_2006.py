# Generated by Django 3.0.8 on 2020-08-05 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20200803_0848'),
    ]

    operations = [
        migrations.CreateModel(
            name='userform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('sw', 'sportswear'), ('s', 'shirt'), ('ow', 'outwear')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('r', 'danger'), ('s', 'secondary'), ('p', 'primary')], max_length=1),
        ),
    ]
