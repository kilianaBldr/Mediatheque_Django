from django import forms
from.models import Membre, Media


class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'prenom', 'email', 'telephone']


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['titre', 'type_media', 'auteur', 'realisateur', 'artiste', 'fabricant', 'disponible']

    def clean(self):
        cleaned_data = super().clean()
        type_media = cleaned_data.get('media_type')

        # Vérifier que le champ spécifique est renseigné en fonction du type de média
        if type_media == 'livre' and not cleaned_data.get('auteur'):
            self.add_error('auteur', "L'auteur est requis pour un livre.")
        elif type_media == 'dvd' and not cleaned_data.get('realisateur'):
            self.add_error('realisateur', "Le réalisateur est requis pour un DVD.")
        elif type_media == 'cd' and not cleaned_data.get('artiste'):
            self.add_error('artiste', "L'artiste est requis pour un CD.")
        elif media_type == 'jeu' and not cleaned_data.get('fabricant'):
            self.add_error('fabricant', "Le fabricant est requis pour un jeu de plateau.")

        return cleaned_data