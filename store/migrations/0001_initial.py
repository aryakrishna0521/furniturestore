# Generated by Django 5.1.5 on 2025-01-22 08:23

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_verified', models.BooleanField(default=False)),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
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
            name='Category',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.basemodel')),
                ('name', models.CharField(max_length=100)),
            ],
            bases=('store.basemodel',),
        ),
        migrations.CreateModel(
            name='Colour',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.basemodel')),
                ('name', models.CharField(max_length=100)),
            ],
            bases=('store.basemodel',),
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.basemodel')),
                ('name', models.CharField(max_length=100)),
            ],
            bases=('store.basemodel',),
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.basemodel')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('store.basemodel',),
        ),
        migrations.CreateModel(
            name='Furniture',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.basemodel')),
                ('name', models.CharField(max_length=255, null=True)),
                ('code', models.CharField(max_length=100, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('price', models.FloatField(null=True)),
                ('picture', models.ImageField(null=True, upload_to='images/')),
                ('category_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.category')),
                ('color_object', models.ManyToManyField(to='store.colour')),
                ('type_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.type')),
            ],
            bases=('store.basemodel',),
        ),
        migrations.CreateModel(
            name='BasketItem',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.basemodel')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('is_order_placed', models.BooleanField(default=False)),
                ('Basket_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_item', to='store.basket')),
                ('product_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.furniture')),
            ],
            bases=('store.basemodel',),
        ),
    ]
