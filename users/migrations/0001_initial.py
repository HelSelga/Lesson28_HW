# Generated by Django 4.0.6 on 2022-07-20 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=8)),
                ('lng', models.DecimalField(decimal_places=6, max_digits=8)),
            ],
            options={
                'verbose_name': 'Локация',
                'verbose_name_plural': 'Локации',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=10)),
                ('last_name', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('username', models.CharField(db_index=True, max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('role', models.CharField(choices=[('member', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Админ')], default='member', max_length=10)),
                ('age', models.PositiveSmallIntegerField()),
                ('locations', models.ManyToManyField(to='users.location')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['username'],
            },
        ),
    ]
