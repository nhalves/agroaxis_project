# Generated by Django 5.2.4 on 2025-07-04 00:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('herd', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MilkQuality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Data da Análise')),
                ('ccs', models.PositiveIntegerField(verbose_name='CCS (x1000)')),
                ('cbt', models.PositiveIntegerField(verbose_name='CBT (x1000)')),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='milk_quality_records', to='herd.animal')),
            ],
            options={
                'verbose_name': 'Análise de Qualidade do Leite',
                'verbose_name_plural': 'Análises de Qualidade do Leite',
                'ordering': ['-date'],
            },
        ),
    ]
