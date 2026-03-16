from django.urls import path
from league_tracker import views

urlpatterns = [

    path('', views.league_list),
    path('league_tracker/league/', views.league_list),
    path('league_tracker/league/<int:pk>', views.getLeague),
    path('league_tracker/decks/', views.decks),
    path('league_tracker/decks/<int:pk>', views.getDeck),
    path('league_tracker/formats/', views.formats),
    path('league_tracker/formats/<int:pk>', views.getFormat),
    path('league_tracker/league_players/', views.league_players),
    path('league_tracker/league_players/<int:pk>', views.getLeaguePlayer),
    path('league_tracker/matches/', views.matches),
    path('league_tracker/matches/<int:pk>', views.getMatches),
    path('league_tracker/match_player_details/', views.match_player_details),
    path('league_tracker/match_player_details/<int:pk>/', views.getMatchPlayerDetail)

]