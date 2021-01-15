# Generated by Django 2.2.11 on 2021-01-13 06:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ourproperty', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_roll', models.CharField(choices=[('dealer', 'Dealer'), ('enduser', 'EndUser')], default='enduser', max_length=20)),
                ('mobile', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_type', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='estateproperty',
            name='dealer',
        ),
        migrations.RemoveField(
            model_name='estateproperty',
            name='property_user',
        ),
        migrations.AddField(
            model_name='estateproperty',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='property_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='PropertyUser',
        ),
        migrations.AddField(
            model_name='estateproperty',
            name='user_type',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='property_user_type', to='ourproperty.UserType'),
        ),
    ]