from django.test import TestCase
from django.urls import reverse
from bibliothecaire.models import Media

class MembreMediaTests(TestCase):

    def setUp(self):
        # Crée deux médias pour les tests
        Media.objects.create(titre="Livre 1", type_media="Livre", disponible=True)
        Media.objects.create(titre="DVD 1", type_media="DVD", disponible=False)

    def test_liste_medias_membre(self):
        # Test pour s'assurer que la liste des médias s'affiche correctement pour un membre
        response = self.client.get(reverse('liste_medias_membre'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Livre 1")
        self.assertContains(response, "DVD 1")
        self.assertContains(response, "Disponible")
        self.assertContains(response, "Indisponible")