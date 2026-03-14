from django.contrib import admin
from .models import Format, League, Deck, League_Player, Match, Match_Player_Detail, Match_Round, Match_Round_Player

class FormatList(admin.ModelAdmin):
    list_display = ('pk', 'name', 'players_per_match', 'rounds_per_match')
    list_filter = ('name', 'players_per_match', 'rounds_per_match')
    search_fields = ('name',)
    ordering = ['name']

class LeagueList(admin.ModelAdmin):
    list_display = ('pk', 'owner', 'format', 'name', 'status', 'decks_per_user', 'start_date', 'end_date', 'match_qty',
        'points_win', 'points_loss', 'points_draw')
    list_filter = ('format', 'name')
    search_fields = ('format', 'name')
    ordering = ['name']

class DeckList(admin.ModelAdmin):
    list_display = ('pk', 'name', 'league_player', 'url')
    list_filter = ('name', 'league_player')
    search_fields = ('name', 'league_player')
    ordering = ['name']

class League_PlayerList(admin.ModelAdmin):
    list_display = ('league', 'player', 'league_player_points')
    list_filter = ('league', 'player')
    search_fields = ('league', 'player')
    ordering = ['league']

class MatchList(admin.ModelAdmin):
    list_display = ('league','number', 'status')
    list_filter = ('league','number', 'status')
    search_fields = ('league','number', 'status')
    ordering = ['league']

class Match_Player_DetailList(admin.ModelAdmin):
    list_display = ('pk', 'match', 'league_player', 'deck')
    list_filter = ('match', 'league_player')
    search_fields = ('match', 'league_player', 'deck')
    ordering = ['match']

class Match_RoundList(admin.ModelAdmin):
    list_display = ('match', 'number', 'status')
    list_filter = ('match', 'number', 'status')
    search_fields = ('match', 'number', 'status')
    ordering = ['match']

class Match_Round_PlayerList(admin.ModelAdmin):
    list_display = ('round','player', 'result', 'points')
    list_filter = ('round','player', 'result')
    search_fields = ('round','player', 'result')
    ordering = ['round']


admin.site.register(Format, FormatList)
admin.site.register(League, LeagueList)
admin.site.register(Deck, DeckList)
admin.site.register(League_Player, League_PlayerList)
admin.site.register(Match, MatchList)
admin.site.register(Match_Player_Detail, Match_Player_DetailList)
admin.site.register(Match_Round, Match_RoundList)
admin.site.register(Match_Round_Player, Match_Round_PlayerList)
