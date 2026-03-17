from django.urls import path
from league_tracker import views

urlpatterns = [

    path('', views.league_list),
    path('league_tracker/leagues/', views.league_list),
    path('league_tracker/league/<int:pk>', views.getLeague),
    path('league_tracker/decks/', views.decks),
    path('league_tracker/deck/<int:pk>', views.getDeck),
    path('league_tracker/formats/', views.formats),
    path('league_tracker/format/<int:pk>', views.getFormat),
    path('league_tracker/league_players/', views.league_players),
    path('league_tracker/league_player/<int:pk>', views.getLeaguePlayer),
    path('league_tracker/matches/', views.matches),
    path('league_tracker/match/<int:pk>', views.getMatches),
    path('league_tracker/match_players/', views.match_player_details),
    path('league_tracker/match_player/<int:pk>/', views.getMatchPlayerDetail),
    path('league_tracker/match_rounds/', views.match_rounds),
    path('league_tracker/match_round/<int:pk>', views.getMatchRoundDetail),
    path('league_tracker/match_round_players/', views.match_round_players),
    path('league_tracker/match_round_player/<int:pk>', views.getMatchRoundPlayerDetail)

]