from django.contrib import admin
from .models import Membre, Media, Emprunt

class MembreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'date_inscription')
    search_fields = ('nom', 'prenom', 'email')

class MediaAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_media', 'disponible')
    list_filter = ('type_media', 'disponible')
    search_fields = ('titre',)

class EmpruntAdmin(admin.ModelAdmin):
    list_display = ('media', 'membre', 'date_emprunt', 'date_retour')
    list_filter = ('date_emprunt', 'date_retour')
    search_fields = ('media__titre', 'membre__nom')

admin.site.register(Membre, MembreAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Emprunt, EmpruntAdmin)