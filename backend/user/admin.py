from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_wins', 'total_games', 'streak', 'win_rate')
    readonly_fields = ('win_rate',)
