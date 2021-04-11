from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ReadyStatus(models.Model):
    status = models.BooleanField(default=True)
    closed_date = models.DateField(verbose_name='Дата закрытия заявки', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.status:
            self.closed_date = None
        super().save(*args, **kwargs)


class CheckStatus(models.Model):
    STATUS = (
        ('accepted', 'Заявка принята'),
        ('rejected', 'Заявка отклонена'),
        ('revision', 'Заявка отправлена на доработку'),
    )
    status = models.CharField(default=False, max_length=8)
    check_date = models.DateField(verbose_name='Дата оценки заявки')
    application = models.ForeignKey('Application', verbose_name='Статус проверки заявки', blank=True, null=True,
                                    on_delete=models.CASCADE)


class Application(models.Model):
    owner = models.OneToOneField(User, verbose_name='Владелец заявки')
    start_date = models.DateField(auto_now_add=True, verbose_name='Старт подачи заявки')
    ready = models.OneToOneField(ReadyStatus, verbose_name='Статус заполнения заявки')
