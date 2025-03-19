from django.contrib import admin
from .models import Team, Player, Match, Owner, Coach

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Owner)
admin.site.register(Coach)
