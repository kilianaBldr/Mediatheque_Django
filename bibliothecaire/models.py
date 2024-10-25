from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

class Membre(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    telephone = models.CharField(max_length=15)
    date_inscription = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def a_des_emprunts_en_retard(self):
        emprunts = self.emprunt_set.filter(date_retour__isnull=True)
        for emprunt in emprunts:
            if emprunt.date_emprunt + timedelta(weeks=1) < timezone.now().date():
                return True
        return False

    def nombre_emprunts_actifs(self):
        return self.emprunt_set.filter(date_retour__isnull=True).count()

class Media(models.Model):
    TYPE_CHOICES = [
        ('Livre', 'Livre'),
        ('CD', 'CD'),
        ('DVD', 'DVD'),
        ('Jeu', 'Jeu de plateau'),
    ]
    titre = models.CharField(max_length=200)
    type_media = models.CharField(max_length=50, choices=TYPE_CHOICES)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titre

class Emprunt(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    date_emprunt = models.DateField(auto_now_add=True)
    date_retour = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.media.titre} emprunté par {self.membre.prenom} {self.membre.nom}"

    def clean(self):
        if self.membre.nombre_emprunts_actifs() >= 3:
            raise ValidationError(f"{self.membre.prenom} {self.membre.nom} a déjà 3 emprunts actifs.")
        if self.membre.a_des_emprunts_en_retard():
            raise ValidationError(f"{self.membre.prenom} {self.membre.nom} a des emprunts en retard et ne peut plus emprunter.")
        if self.media.type_media == 'Jeu':
            raise ValidationError("Les jeux de plateau ne peuvent pas être empruntés.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)