from django import forms
from.models import Membre, Media


class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'prenom', 'email', 'telephone']


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['titre', 'type_media', 'disponible']