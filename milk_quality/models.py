from django.db import models
from herd.models import Animal
from django.contrib.auth.models import User

class MilkQuality(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='milk_records', null=True, blank=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='milk_quality_records')
    date = models.DateField(verbose_name="Data da Análise")
    ccs = models.PositiveIntegerField(verbose_name="CCS (x1000)")
    cbt = models.PositiveIntegerField(verbose_name="CBT (x1000)")
    production_volume = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Volume de Produção (Litros)")

    class Meta:
        verbose_name = "Análise de Qualidade do Leite"
        verbose_name_plural = "Análises de Qualidade do Leite"
        ordering = ['-date']

    def __str__(self):
        return f'Análise de {self.animal.name} em {self.date.strftime("%d/%m/%Y")}'