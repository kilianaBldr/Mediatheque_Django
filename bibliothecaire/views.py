from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Membre, Media, Emprunt
from .forms import MembreForm, MediaForm

def liste_membres(request):
    membres = Membre.objects.all()
    return render(request, 'bibliothecaire/liste_membres.html', {'membres': membres})

def creer_membre(request):
    if request.method == "POST":
        form = MembreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Membre créé avec succès.")
            return redirect('liste_membres')
    else:
        form = MembreForm()
    return render(request, 'bibliothecaire/creer_membre.html', {'form': form})

def mise_a_jour_membre(request, id):
    membre = get_object_or_404(Membre, id=id)
    if request.method == "POST":
        form = MembreForm(request.POST, instance=membre)
        if form.is_valid():
            form.save()
            messages.success(request, "Membre mis à jour avec succès.")
            return redirect('liste_membres')
    else:
        form = MembreForm(instance=membre)
    return render(request, 'bibliothecaire/mise_a_jour_membre.html', {'form': form})

def liste_medias(request):
    medias = Media.objects.all()
    return render(request, 'bibliothecaire/liste_medias.html', {'medias': medias})

def creer_media(request):
    if request.method == "POST":
        form = MediaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Média ajouté avec succès.")
            return redirect('liste_medias')
    else:
        form = MediaForm()
    return render(request, 'bibliothecaire/creer_media.html', {'form': form})

def creer_emprunt(request, media_id):
    media = get_object_or_404(Media, id=media_id)
    membres = Membre.objects.all()
    if request.method == "POST":
        membre_id = request.POST.get("membre")
        membre = get_object_or_404(Membre, id=membre_id)

        try:
            emprunt = Emprunt(media=media, membre=membre)
            emprunt.clean()
            emprunt.save()

            media.disponible = False
            media.save()

            messages.success(request, f"{media.titre} a été emprunté par {membre.prenom} {membre.nom}.")
            return redirect('liste_medias')
        except ValidationError as e:
            messages.error(request, e.message)

    return render(request, 'bibliothecaire/creer_emprunt.html', {'media': media, 'membres': membres})

def retourner_emprunt(request, emprunt_id):
    emprunt = get_object_or_404(Emprunt, id=emprunt_id)
    emprunt.media.disponible = True
    emprunt.media.save()
    emprunt.date_retour = timezone.now()
    emprunt.save()
    messages.success(request, "L'emprunt a été retourné avec succès.")
    return redirect('liste_medias')