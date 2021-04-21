# Generated by Django 3.1.7 on 2021-04-21 18:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now_add=True, verbose_name='Старт подачи заявки')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец заявки')),
            ],
        ),
        migrations.CreateModel(
            name='ReadyStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('closed_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия заявки')),
            ],
        ),
        migrations.CreateModel(
            name='CheckStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('accepted', 'Заявка принята'), ('rejected', 'Заявка отклонена'), ('revision', 'Заявка отправлена на доработку')], max_length=8)),
                ('check_date', models.DateTimeField(verbose_name='Дата оценки заявки')),
                ('application', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.application', verbose_name='Статус проверки заявки')),
                ('judge', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='ready',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_app.readystatus', verbose_name='Статус заполнения заявки'),
        ),
    ]
