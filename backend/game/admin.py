from django.contrib import admin
from .models import GameHistory

@admin.register(GameHistory)
class GameHistoryAdmin(admin.ModelAdmin):
    list_display = ('player', 'player_choice', 'cpu_choice', 'result', 'created_at')
    list_filter = ('result', 'player_choice', 'cpu_choice')
    search_fields = ('player__username',)
    readonly_fields = ('created_at',)
