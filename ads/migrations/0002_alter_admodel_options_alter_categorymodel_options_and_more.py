# Generated by Django 4.0.6 on 2022-07-20 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admodel',
            options={'verbose_name': 'Объявление', 'verbose_name_plural': 'Объявления'},
        ),
        migrations.AlterModelOptions(
            name='categorymodel',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.RemoveField(
            model_name='admodel',
            name='address',
        ),
        migrations.AddField(
            model_name='admodel',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ads.categorymodel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='admodel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
        migrations.AlterField(
            model_name='admodel',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
    ]
