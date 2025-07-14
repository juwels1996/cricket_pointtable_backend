from django.contrib import admin
from .models import Team, Player, Match, Owner, Coach
from .models import YouTubeVideo
from .models import Adviser
from .models import PDF
from .models import Sponsor
from .models import PlayerRegistration

class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_link', 'thumbnail_url', 'created_at')  # Fields to display in the list view
    search_fields = ['title']  # Allow searching by title
    list_filter = ['created_at']

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'category', 'runs', 'matches')
    list_filter = ('category',)
    search_fields = ('name',)

class AdviserAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation')  # Show name and designation in the list view
    search_fields = ['name', 'designation']

class PlayerRegistrationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone_number', 'address', 'area', 'speciality', 'player_category', 'player_photo']
    list_filter = ['area', 'player_category', 'speciality']
    search_fields = ['name', 'phone_number', 'address'] 

admin.site.register(Team)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Match)
admin.site.register(Owner)
admin.site.register(Coach)
admin.site.register(YouTubeVideo, YouTubeVideoAdmin)
admin.site.register(Adviser, AdviserAdmin)
admin.site.register(PDF)
admin.site.register(Sponsor)
admin.site.register(PlayerRegistration, PlayerRegistrationAdmin)

