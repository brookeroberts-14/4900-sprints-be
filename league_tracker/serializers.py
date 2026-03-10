from django.contrib.auth.models import User
from .models import Format, League, League_Player, Deck, Match, Match_Player_Detail, Match_Round, Match_Round_Player
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

## We will need to adjust this so it is related to our Model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'is_superuser', 'first_name', 'last_name', 'email')

class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ('pk', 'name', 'players_per_match', 'rounds_per_match')

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        status_display = serializers.CharField(source='get_status_display', read_only=True)
        fields = ('pk', 'owner', 'format', 'name', 'status', 'decks_per_user', 'start_date',
                  'end_date', 'match_qty', 'points_win', 'points_loss', 'points_draw')