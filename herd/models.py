from django.db import models
from django.contrib.auth.models import User

class Animal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='animals', null=True, blank=True)
    STATUS_CHOICES = (
        ('lactation', 'Em Lactação'),
        ('dry', 'Seca'),
        ('heifer', 'Novilha'),
        ('calf', 'Bezerra'),
    )

    earring = models.CharField(max_length=20, unique=True, verbose_name="Brinco")
    name = models.CharField(max_length=100, verbose_name="Nome")
    birth_date = models.DateField(verbose_name="Data de Nascimento")
    breed = models.CharField(max_length=50, blank=True, null=True, verbose_name="Raça")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lactation')
    # O campo 'photo' será adicionado em uma fase futura para simplificar o MVP.

    def __str__(self):
        return f'{self.name} ({self.earring})'

class ReproductiveEvent(models.Model):
    EVENT_TYPE_CHOICES = (
        ('heat', 'Cio'),
        ('insemination', 'Inseminação/Cobertura'),
        ('pregnancy_diagnosis', 'Diagnóstico de Gestação'),
        ('calving', 'Parto'),
    )
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='reproductive_events')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reproductive_events', null=True, blank=True)
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES)
    event_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Evento Reprodutivo"
        verbose_name_plural = "Eventos Reprodutivos"
        ordering = ['-event_date']

    def __str__(self):
        return f'{self.event_type} - {self.animal.name} em {self.event_date}'

class HealthEvent(models.Model):
    EVENT_TYPE_CHOICES = (
        ('vaccination', 'Vacinação'),
        ('treatment', 'Tratamento'),
        ('disease', 'Doença'),
    )
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='health_events')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_events', null=True, blank=True)
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES)
    event_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    medication = models.CharField(max_length=100, blank=True, null=True)
    withdrawal_period_days = models.PositiveIntegerField(blank=True, null=True, verbose_name="Período de Carência (dias)")

    class Meta:
        verbose_name = "Evento Sanitário"
        verbose_name_plural = "Eventos Sanitários"
        ordering = ['-event_date']

    def __str__(self):
        return f'{self.event_type} - {self.animal.name} em {self.event_date}'