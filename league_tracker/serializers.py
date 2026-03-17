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
    # 1. Define custom fields at the top of the class
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    format = FormatSerializer(read_only=True) # 'format' field is nested

    class Meta:
        model = League
        fields = ('pk', 'owner', 'format', 'name', 'status', 'status_display', 'decks_per_user', 'start_date',
                  'end_date', 'match_qty', 'points_win', 'points_loss', 'points_draw')
        read_only_fields = ('owner', 'status',)

class LeaguePlayerSerializer(serializers.ModelSerializer):
    league_name = serializers.ReadOnlyField(source='league.name')
    player_name = serializers.ReadOnlyField(source='player.username')
    format = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = League_Player
        fields = ('pk', 'league', 'format', 'league_name', 'player', 'player_name', 'league_player_points')
        read_only_fields = ('league_player_points',)

class DeckSerializer(serializers.ModelSerializer):
    player_username = serializers.ReadOnlyField(source='player.username')
    league_name = serializers.ReadOnlyField(source='league.name')
    league_player = LeaguePlayerSerializer(read_only=True) # league_player is nested

    class Meta:
        model = Deck
        fields = ('pk', 'league_player', 'name', 'url', 'player_username', 'league_name')

    def validate(self, data):
        ##Check that the player hasn't exceeded the deck limit for this league.
        league_player = data.get('league_player')

        # Access the limit through the ForeignKey chain: League_Player -> League
        limit = league_player.league.decks_per_user

        # Count existing decks for this player in this league
        # If we are updating an existing deck, we exclude it from the count
        existing_count = Deck.objects.filter(league_player=league_player)
        if self.instance:
            existing_count = existing_count.exclude(pk=self.instance.pk)

        if existing_count.count() >= limit:
            raise serializers.ValidationError(
                f"Deck limit reached ({limit}) for this league."
            )

        return data

class MatchPlayerDetailSerializer(serializers.ModelSerializer):
    player_name = serializers.ReadOnlyField(source='league_player.player.username')
    deck_name = serializers.ReadOnlyField(source='deck.name')

    class Meta:
        model = Match_Player_Detail
        fields = ('pk', 'match', 'league_player', 'player_name', 'deck', 'deck_name')

        def validate(self, data):
            ## I replicated the model's clean() logic for the API.
            match = data.get('match')
            league_player = data.get('league_player')
            deck = data.get('deck')

            # 1. Ensure the Player is actually enrolled in the League this Match belongs to
            if match and league_player:
                if match.league_id != league_player.league_id:
                    raise serializers.ValidationError(
                        {"league_player": "This player is not enrolled in this match's league."}
                    )

            # 2. Ensure the selected Deck actually belongs to this League Player
            if deck and league_player:
                if deck.league_player_id != league_player.id:
                    raise serializers.ValidationError(
                        {"deck": "This deck does not belong to the selected player."}
                    )

            return data

class MatchRoundSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = Match_Round
        fields = ('pk', 'match', 'number', 'status', 'status_display')

class MatchSerializer(serializers.ModelSerializer):
    participants = MatchPlayerDetailSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    rounds = MatchRoundSerializer(many=True, read_only=True)
    league_name = serializers.ReadOnlyField(source='league.name')

    class Meta:
        model = Match
        fields = ('pk', 'league', 'league_name', 'number', 'status', 'status_display', 'rounds', 'participants')


class MatchRoundPlayerSerializer(serializers.ModelSerializer):
    result_display = serializers.CharField(source='get_result_display', read_only=True)
    player_username = serializers.ReadOnlyField(source='player.league_player.player.username')

    class Meta:
        model = Match_Round_Player
        fields = ('pk', 'round', 'player', 'player_username', 'result', 'result_display', 'points')
        # Points are calculated in the model's save() method, so we don't manually input them
        read_only_fields = ('points',)

    def validate(self, data):
        ## I replicated the clean() method to ensure the player is actually in this match.
        round_obj = data.get('round')
        player_detail = data.get('player')

        if round_obj and player_detail:
            if round_obj.match_id != player_detail.match_id:
                raise serializers.ValidationError(
                    "This player is not a registered participant of the match this round belongs to."
                )
        return data