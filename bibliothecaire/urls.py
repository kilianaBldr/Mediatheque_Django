from django.urls import path
from .views import liste_membres, creer_membre, mise_a_jour_membre, liste_medias, creer_media, creer_emprunt, retourner_emprunt


urlpatterns = [
    path('membres/', liste_membres, name='liste_membres'),
    path('creer_membre/', creer_membre, name='creer_membre'),
    path('membres/<int:id>/modifier/', mise_a_jour_membre, name='mise_a_jour_membre'),
    path('medias/', liste_medias, name='liste_medias'),
    path('creer_medias', creer_media, name='creer_media'),
    path('medias/<int:media_id>/emprunter/', creer_emprunt, name='creer_emprunt'),
    path('emprunts/<int:emprunt_id>/retourner/', retourner_emprunt, name='retourner_emprunt'),
]