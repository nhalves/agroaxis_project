from django.test import TestCase
from .models import Transaction
from decimal import Decimal

# Exemplo de uma função que poderia existir em `utils.py` ou `models.py`
def calcular_custo_por_litro(mes, ano, usuario):
    """
    Calcula o custo de produção por litro de leite para um determinado mês e ano.
    """
    despesas_totais = Transaction.objects.filter(
        user=usuario,
        date__year=ano,
        date__month=mes,
        transaction_type='despesa'
    ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')

    # Supondo que o volume de leite seja armazenado em outro modelo ou obtido de outra forma.
    # Para este exemplo, vamos usar um valor fixo.
    volume_leite_mes = Decimal('10000') # 10.000 litros

    if volume_leite_mes == 0:
        return Decimal('0.00')

    custo_por_litro = despesas_totais / volume_leite_mes
    return round(custo_por_litro, 2)

class FinanceiroCalculosTest(TestCase):

    def setUp(self):
        """Cria um usuário e transações de exemplo para os testes."""
        from django.contrib.auth.models import User
        self.user = User.objects.create_user(username='produtor_teste', password='123')

        # Despesas de exemplo
        Transaction.objects.create(user=self.user, amount=Decimal('1500.00'), category='Alimentação', transaction_type='despesa', date='2025-07-15')
        Transaction.objects.create(user=self.user, amount=Decimal('500.00'), category='Sanidade', transaction_type='despesa', date='2025-07-20')
        Transaction.objects.create(user=self.user, amount=Decimal('1000.00'), category='Outros', transaction_type='despesa', date='2025-07-25')

        # Receita de exemplo (não deve entrar no cálculo de custo)
        Transaction.objects.create(user=self.user, amount=Decimal('20000.00'), category='Venda de Leite', transaction_type='receita', date='2025-07-28')

    def test_calculo_custo_por_litro(self):
        """
        Testa se o cálculo do custo por litro está correto com base nas despesas lançadas.
        Volume de leite fixo em 10.000 litros para este teste.
        Custo total = 1500 + 500 + 1000 = 3000
        Custo por litro = 3000 / 10000 = 0.30
        """
        # Nota: A função `calcular_custo_por_litro` é um exemplo e não existe no código ainda.
        # Este teste serve como um guia para quando ela for implementada.
        
        # Simulando a lógica da função para o teste
        despesas_totais = sum([t.amount for t in Transaction.objects.filter(user=self.user, transaction_type='despesa')])
        volume_leite = Decimal('10000')
        custo_calculado = round(despesas_totais / volume_leite, 2)

        self.assertEqual(custo_calculado, Decimal('0.30'))

    def test_custo_sem_despesas(self):
        """Testa o cálculo quando não há despesas no mês."""
        Transaction.objects.filter(user=self.user, transaction_type='despesa').delete()
        
        despesas_totais = sum([t.amount for t in Transaction.objects.filter(user=self.user, transaction_type='despesa')])
        volume_leite = Decimal('10000')
        custo_calculado = round(despesas_totais / volume_leite, 2) if volume_leite > 0 else 0

        self.assertEqual(custo_calculado, Decimal('0.00'))