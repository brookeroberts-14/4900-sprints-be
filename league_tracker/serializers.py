from django.contrib.auth.models import User
from .models import Format, League, League_Player, Deck, Match, Match_Player_Detail, Match_Round, Match_Round_Player
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'write_only': True, 'min_length': 6},
            'password2': {'write_only': True, 'min_length': 6}
        }
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

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
    #I had to change how format was read for the league creation on the FE. Setting it to read-only made it so new
    #leagues couldn't set their format which gave a 500 error.
    format = serializers.PrimaryKeyRelatedField(queryset=Format.objects.all(),write_only=True)
    format_details = FormatSerializer(source='format', read_only=True)

    class Meta:
        model = League
        fields = ('pk', 'owner', 'format', 'format_details', 'name', 'status', 'status_display', 'decks_per_user', 'start_date',
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
    player_name = serializers.ReadOnlyField(source='league_player.player.username')
    league_id = serializers.ReadOnlyField(source='league_player.league.id')

    league_player = serializers.PrimaryKeyRelatedField(queryset=League_Player.objects.all())

    class Meta:
        model = Deck
        fields = ('pk', 'league_player', 'name', 'url', 'player_name', 'league_id')

    def validate(self, data):
        league_player = data.get('league_player')

        if not league_player:
            raise serializers.ValidationError("League player is required.")

        limit = league_player.league.decks_per_user

        existing_count = Deck.objects.filter(league_player=league_player)
        if self.instance:
            existing_count = existing_count.exclude(pk=self.instance.pk)

        if existing_count.count() >= limit:
            raise serializers.ValidationError(
                f"Deck limit reached ({limit}) for this player in this league."
            )

        return data

class MatchPlayerDetailSerializer(serializers.ModelSerializer):
    player_name = serializers.ReadOnlyField(source='league_player.player.username')
    player_username = serializers.ReadOnlyField(source='league_player.player.username')
    deck_name = serializers.ReadOnlyField(source='deck.name')

    class Meta:
        model = Match_Player_Detail
        fields = ('pk', 'match', 'league_player', 'player_name', 'player_username', 'deck', 'deck_name')

    def validate(self, data):
        match = data.get('match')
        league_player = data.get('league_player')
        deck = data.get('deck')

        if match and league_player:
            if match.league_id != league_player.league_id:
                raise serializers.ValidationError(
                    {"league_player": "This player is not enrolled in this match's league."}
                )

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