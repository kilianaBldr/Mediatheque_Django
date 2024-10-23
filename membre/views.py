from django.shortcuts import render
from bibliothecaire.models import Media


def liste_medias(request):
        medias = Media.objects.all()
        return  render(request, 'membre/liste_medias.html',
                       {'medias': medias})
