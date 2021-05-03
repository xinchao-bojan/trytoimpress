from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ReadyStatus(models.Model):
    status = models.BooleanField(default=True)
    closed_date = models.DateTimeField(verbose_name='Дата закрытия заявки', blank=True, null=True)
    application = models.OneToOneField('Application', verbose_name='Статус заполнения заявки', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.status:
            self.closed_date = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.application} ready'


class CheckStatus(models.Model):
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    REVISION = 'revision'
    STATUS = (
        (ACCEPTED, 'Заявка принята'),
        (REJECTED, 'Заявка отклонена'),
        (REVISION, 'Заявка отправлена на доработку'),
    )

    judge = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=STATUS, max_length=8)
    check_date = models.DateTimeField(verbose_name='Дата оценки заявки')
    application = models.ForeignKey('Application', verbose_name='Статус проверки заявки', blank=True, null=True,
                                    on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.application} check'


class Application(models.Model):
    owner = models.ForeignKey(User, verbose_name='Владелец заявки', on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True, verbose_name='Старт подачи заявки')

    def __str__(self):
        return self.owner.name
