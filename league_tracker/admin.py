from django.contrib import admin
from .models import Format, League, Deck, League_Player, Match, Match_Player_Detail, Match_Round, Match_Round_Player

class FormatList(admin.ModelAdmin):
    list_display = ('pk', 'name', 'players_per_match', 'rounds_per_match')
    list_filter = ('name', 'players_per_match', 'rounds_per_match')
    search_fields = 'name'
    ordering = ['name']

class LeagueList(admin.ModelAdmin):
    list_display = ('pk', 'owner', 'format', 'name', 'status', 'decks_per_user', 'start_date', 'end_date', 'match_qty',
        'points_win', 'points_loss', 'points_draw')
    list_filter = ('format', 'name')
    search_fields = ('format', 'name')
    ordering = ['name']

class DeckList(admin.ModelAdmin):
    list_display = ('pk', 'name', 'players_per_match', 'rounds_per_match')
    list_filter = ('name', 'players_per_match', 'rounds_per_match')
    search_fields = 'name'
    ordering = ['name']

class League_PlayerList(admin.ModelAdmin):
    list_display = ('customer', 'category', 'description', 'recent_value')
    list_filter = ('customer', 'category')
    search_fields = ('customer', 'category')
    ordering = ['customer']

class MatchList(admin.ModelAdmin):
    list_display = ('customer','symbol', 'name', 'shares', 'purchase_price')
    list_filter = ('customer','symbol', 'name')
    search_fields = ('customer','symbol', 'name')
    ordering = ['customer']

class Match_Player_DetailList(admin.ModelAdmin):
    list_display = ('pk', 'name', 'players_per_match', 'rounds_per_match')
    list_filter = ('name', 'players_per_match', 'rounds_per_match')
    search_fields = 'name'
    ordering = ['name']

class Match_RoundList(admin.ModelAdmin):
    list_display = ('customer', 'category', 'description', 'recent_value')
    list_filter = ('customer', 'category')
    search_fields = ('customer', 'category')
    ordering = ['customer']

class Match_Round_PlayerList(admin.ModelAdmin):
    list_display = ('customer','symbol', 'name', 'shares', 'purchase_price')
    list_filter = ('customer','symbol', 'name')
    search_fields = ('customer','symbol', 'name')
    ordering = ['customer']


admin.site.register(Format, FormatList)
admin.site.register(League, LeagueList)
admin.site.register(Deck, DeckList)
admin.site.register(League_Player, League_PlayerList)
admin.site.register(Match, MatchList)
admin.site.register(Match_Player_Detail, Match_Player_DetailList)
admin.site.register(Match_Round, Match_RoundList)
admin.site.register(Match_Round_Player, Match_Round_PlayerList)
