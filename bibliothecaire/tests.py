from django.test import TestCase
from django.urls import reverse
from .models import Membre, Media


class MembreTests(TestCase):

    def setUp(self):
        # Crée un membre pour les tests
        self.membre = Membre.objects.create(nom="Dupont", prenom="Jean", email="jean.dupont@example.com")

    def test_creer_membre(self):
        # Test pour vérifier que la page de création de membre fonctionne
        response = self.client.get(reverse('creer_membre'))
        self.assertEqual(response.status_code, 200)
        # Création d'un membre via le formulaire
        response = self.client.post(reverse('creer_membre'), {
            'nom': 'Martin',
            'prenom': 'Pierre',
            'email': 'pierre.martin@example.com',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Membre.objects.count(), 2)

    def test_mise_a_jour_membre(self):
        # Test de la mise à jour d'un membre existant
        response = self.client.post(reverse('mise_a_jour_membre', args=[self.membre.id]), {
            'nom': 'Durand',
            'prenom': 'Jean',
            'email': 'jean.durand@example.com',
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

    def test_creer_media(self):
        # Test pour vérifier que la page de création de média fonctionne
        response = self.client.get(reverse('creer_media'))
        self.assertEqual(response.status_code, 200)
        # Création d'un média via le formulaire
        response = self.client.post(reverse('creer_media'), {
            'titre': 'Nouveau Livre',
            'type_media': 'Livre',
            'disponible': True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Media.objects.count(), 2)

    def test_liste_medias(self):
        # Test pour s'assurer que la liste des médias s'affiche correctement
        response = self.client.get(reverse('liste_medias'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Livre")