from django.test import TestCase
from django.urls import reverse
from .models import Membre, Media, Emprunt


class MembreTests(TestCase):

    def setUp(self):
        # Crée un membre pour les tests
        self.membre = Membre.objects.create(nom="Dupont", prenom="Jean", email="jean.dupont@example.com", telephone="0746464646")

    def test_creer_membre(self):
        # Test pour vérifier que la page de création de membre fonctionne
        response = self.client.get(reverse('creer_membre'))
        self.assertEqual(response.status_code, 200)
        # Création d'un membre via le formulaire
        response = self.client.post(reverse('creer_membre'), {
            'nom': 'Martin',
            'prenom': 'Pierre',
            'email': 'pierre.martin@example.com',
            'telephone': '0746464646',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Membre.objects.count(), 2)

    def test_mise_a_jour_membre(self):
        # Test de la mise à jour d'un membre existant
        response = self.client.post(reverse('mise_a_jour_membre', args=[self.membre.id]), {
            'nom': 'Durand',
            'prenom': 'Jean',
            'email': 'jean.durand@example.com',
            'telephone': '0746464646',
        })
        self.assertEqual(response.status_code, 302)
        self.membre.refresh_from_db()
        self.assertEqual(self.membre.nom, 'Durand')

    def test_liste_membres(self):
        # Test pour s'assurer que la liste des membres s'affiche correctement
        response = self.client.get(reverse('liste_membres'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jean")


class MediaTests(TestCase):

    def setUp(self):
        # Crée un média pour les tests
        self.media = Media.objects.create(titre="Test Livre", type_media="Livre", disponible=True)

    def test_affichage_liste_medias(self):
        # Test pour s'assurer que la liste des médias s'affiche correctement
        response = self.client.get(reverse('liste_medias'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bibliothecaire/liste_medias.html')
        self.assertContains(response, "Test Livre")

    def test_creation_media(self):
        # Test de la création d'un média
        response = self.client.post(reverse('creer_media'), {
            'titre': 'Nouveau Livre',
            'type_media': 'Livre',
            'disponible': True,
        })
        self.assertEqual(response.status_code, 302) # Redirection après succès
        self.assertEqual(Media.objects.count(), 2) # Vérifie si un nouveau média a été ajouté


class EmpruntTests(TestCase):

    def setUp(self):
        self.membre = Membre.objects.create(nom="Dupont", prenom="Jean", email="jean.dupont@example.com")
        self.media = Media.objects.create(titre="Test Livre", type_media="Livre", disponible=True)
        self.emprunt = Emprunt.objects.create(media=self.media, membre=self.membre)

    def test_creation_emprunt(self):
        # Test de la création d'un emprunt pour un média disponible
        response = self.client.post(reverse('creer_emprunt', args=[self.media.id]), {
            'membre': self.membre.id
        })
        self.assertEqual(response.status_code, 302) # Redirection après création
        self.assertFalse(Media.objects.get(id=self.media.id).disponible) # Le média est maintenant emprunté

    def test_retourner_emprunt(self):
        # Test pour vérifier le retour d'un emprunt
        response = self.client.post(reverse('retourner_emprunt', args=[self.emprunt.id]))
        self.assertEqual(response.status_code, 302)
        self.emprunt.refresh_from_db()
        self.assertIsNotNone(self.emprunt.date_retour) # Vérifie que l'emprunt est marqué comme retourné
        self.assertTrue(Media.objects.get(id=self.media.id).disponible) # Le média est de nouveau disponible