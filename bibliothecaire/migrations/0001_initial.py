# Generated by Django 5.1.2 on 2024-10-23 14:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('type_media', models.CharField(choices=[('Livre', 'Livre'), ('CD', 'CD'), ('DVD', 'DVD'), ('Jeu', 'Jeu de plateau')], max_length=50)),
                ('disponible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Membre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telephone', models.CharField(max_length=15)),
                ('date_inscription', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Emprunt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_emprunt', models.DateField(auto_now_add=True)),
                ('date_retour', models.DateField(blank=True, null=True)),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibliothecaire.media')),
                ('membre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibliothecaire.membre')),
            ],
        ),
    ]
