from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    TRANSACTION_TYPE_CHOICES = (
        ('revenue', 'Receita'),
        ('expense', 'Despesa'),
    )

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, default='expense')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        ordering = ['-date']

    def __str__(self):
        return f'{self.get_type_display()} - R${self.amount} em {self.date.strftime("%d/%m/%Y")}'