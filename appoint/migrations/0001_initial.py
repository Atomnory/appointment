# Generated by Django 3.2 on 2021-05-22 17:50

import appoint.models
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('M', 'Moderator'), ('D', 'Doctor'), ('C', 'Customer')], default='C', max_length=1, verbose_name='Type')),
                ('first_name', models.CharField(max_length=50, verbose_name='First name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last name')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='appoint.user')),
            ],
            options={
                'ordering': ['last_name'],
            },
            bases=('appoint.user',),
            managers=[
                ('objects', appoint.models.CustomerManager()),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='appoint.user')),
                ('specialization', models.CharField(max_length=50, verbose_name='Specialization')),
                ('info', models.TextField(blank=True, max_length=1250, verbose_name='Information')),
            ],
            options={
                'ordering': ['specialization', 'last_name'],
            },
            bases=('appoint.user',),
            managers=[
                ('objects', appoint.models.DoctorManager()),
            ],
        ),
        migrations.CreateModel(
            name='Moderator',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='appoint.user')),
            ],
            options={
                'ordering': ['last_name'],
            },
            bases=('appoint.user',),
            managers=[
                ('objects', appoint.models.ModeratorManager()),
            ],
        ),
        migrations.CreateModel(
            name='DoctorPhoto',
            fields=[
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='appoint.doctor')),
                ('photo', models.ImageField(upload_to='doctor_photo')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(verbose_name='Start time')),
                ('end_time', models.TimeField(verbose_name='End time')),
                ('date', models.DateField(verbose_name='Date')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='appoint.customer')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appoint.doctor')),
            ],
            options={
                'ordering': ['start_time'],
            },
        ),
    ]
