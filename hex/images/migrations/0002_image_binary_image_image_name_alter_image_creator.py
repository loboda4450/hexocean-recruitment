# Generated by Django 4.1.6 on 2023-02-19 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='binary',
            field=models.BinaryField(default=b'XD'),
        ),
        migrations.AddField(
            model_name='image',
            name='image_name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='image',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='images.imagesuser'),
        ),
    ]
