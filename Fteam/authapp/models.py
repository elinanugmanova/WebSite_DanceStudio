from django.conf import settings
from django.db import models


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    abonement = models.ForeignKey('Abonement', on_delete=models.CASCADE, verbose_name='Абонемент',null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f"Покупка {self.abonement.name} от {self.user.username} ({self.created_at})"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'



class Record(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',null=True)
    training = models.ForeignKey('Training', on_delete=models.CASCADE, verbose_name='Тренирока',null=True)

    def __str__(self):
        return (f"Запись на {self.training.specialization} от {self.training.trainer} : "
                f"({self.training.time_start()} - {self.training.time_end()} )")

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class Training(models.Model):
    SPECIALIZATION_CHOICES = [
        ('dh', 'Dancehall'),
        ('hh', 'Hip-Hop'),
        ('cont', 'Contemporary'),
        ('tw', 'twerk'),
        ('vg', 'vogue'),
        ('hs', 'house'),
    ]

    specialization = models.CharField('Направление', max_length=100, choices=SPECIALIZATION_CHOICES)
    date=models.DateField('Дата', null=True)
    time_start = models.TimeField('Время начала', null=True)
    time_end = models.TimeField('Время окончания', null=True)
    gym_number = models.DecimalField('Номер зала', max_digits=10, decimal_places=0)
    trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE, null=True, verbose_name='Тренер')

    def __str__(self):
        return (f"Тренировка по  от {self.trainer.fio}: {self.specialization}"
                f"({self.time_start} - {self.time_end} )")

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'


class Abonement(models.Model):
    name = models.CharField('Название', max_length=50)
    number_of_trainings = models.DecimalField('Количество тренировок', max_digits=10, decimal_places=0)
    price = models.DecimalField('Стоимость', max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} : {self.number_of_trainings} тренировок - {self.price} руб."

    def get_absolute_url(self):
        return f'abonement/{self.id}'

    class Meta:
        verbose_name = 'Абонемент'
        verbose_name_plural = 'Абонементы'


class Trainer(models.Model):
    SPECIALIZATION_CHOICES = [
        ('dh', 'Dancehall'),
        ('hh', 'Hip-Hop'),
        ('cont', 'Contemporary'),
        ('tw', 'twerk'),
        ('vg', 'vogue'),
        ('hs', 'house'),
    ]

    fio = models.CharField('ФИО', max_length=100)
    specialization = models.CharField('Направление', max_length=100, choices=SPECIALIZATION_CHOICES)
    phonenumber = models.CharField('Номер телефона', max_length=12)
    email = models.EmailField('Почта')

    def __str__(self):
        return f"{self.fio} - ({self.specialization})"

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'













