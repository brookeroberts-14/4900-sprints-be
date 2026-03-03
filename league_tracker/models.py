from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Format(models.Model):
    name = models.CharField(max_length=100, unique=True)
    players_per_match = models.PositiveSmallIntegerField()
    rounds_per_match = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.name


class League(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "a", "Active"
        PENDING = "p", "Pending"
        ENDED = "e", "Ended"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    format = models.ForeignKey(Format, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PENDING)
    decks_per_user = models.PositiveSmallIntegerField(default=1)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    match_qty = models.PositiveIntegerField(default=0)
    points_win = models.PositiveIntegerField(default=5)
    points_loss = models.PositiveIntegerField(default=0)
    points_draw = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class League_Player(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    league_player_points = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["league", "player"], name="uq_league_player"),
        ]

    def __str__(self):
        return f"{self.player.username} @ {self.league.name} ({self.league_player_points} pts)"


class Deck(models.Model):
    league_player = models.ForeignKey(League_Player, on_delete=models.CASCADE, related_name="decks")
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["league_player", "name"], name="uq_deck_per_league_player_name"),
        ]

    def clean(self):
        # Enforce max decks per user within the league
        if self.league_player_id and self.league_player.league.decks_per_user:
            existing = Deck.objects.filter(league_player=self.league_player).exclude(pk=self.pk).count()
            if existing >= self.league_player.league.decks_per_user:
                raise ValidationError(f"Deck limit reached ({self.league_player.league.decks_per_user}) for this league.")

    def __str__(self):
        return f"{self.name} ({self.league_player.player.username})"


class Match(models.Model):
    class Status(models.TextChoices):
        PENDING = "p", "Pending"
        COMPLETED = "c", "Completed"

    league = models.ForeignKey(League, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PENDING)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["league", "number"], name="uq_match_number_per_league"),
        ]

    def __str__(self):
        return f"{self.league.name} Match {self.number}"


class Match_Player_Detail(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="participants")
    league_player = models.ForeignKey(League_Player, on_delete=models.PROTECT)
    deck = models.ForeignKey(Deck, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["match", "league_player"], name="uq_match_league_player"),
        ]

    def clean(self):
        # Makes sure the match and player belong to the same league. Could get messy with multiple leagues
        # sharing multiple players.
        if self.match_id and self.league_player_id:
            if self.match.league_id != self.league_player.league_id:
                raise ValidationError("Player is not in this match's league.")
        # Checks if this player in this league has this deck registered. Can be removed if deck selection is handled
        # in the front end.
        if self.deck_id and self.league_player_id:
            if self.deck.league_player_id != self.league_player_id:
                raise ValidationError("Selected deck does not belong to this player in this league.")

    def __str__(self):
        return f"{self.league_player.player.username} in {self.match}"


class Match_Round(models.Model):
    class Status(models.TextChoices):
        COMPLETED = "c", "Completed"
        PENDING = "p", "Pending"

    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="rounds")
    number = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PENDING)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["match", "number"], name="uq_round_number_per_match"),
        ]

    def __str__(self):
        return f"{self.match} - Round {self.number}"


class Match_Round_Player(models.Model):
    class Result(models.TextChoices):
        WIN = "w", "Win"
        DRAW = "d", "Draw"
        LOSS = "l", "Loss"

    round = models.ForeignKey(Match_Round, on_delete=models.CASCADE, related_name="results")
    player = models.ForeignKey(Match_Player_Detail, on_delete=models.CASCADE, related_name="round_results")
    result = models.CharField(max_length=1, choices=Result.choices, default=Result.DRAW)
    points = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["round", "player"], name="uq_round_player_once"),
        ]

    def save(self, *args, **kwargs):
        # Saves points to league_player.points based on match_round_player.result. The amount is from league.points_win
        # league.points_draw or league.point_loss.
        league = self.round.match.league
        if self.result == self.Result.WIN:
            self.points = league.points_win
        elif self.result == self.Result.DRAW:
            self.points = league.points_draw
        else:
            self.points = league.points_loss
        super().save(*args, **kwargs)

    def clean(self):
        # Just makes sure that player belongs to the same match & round.
        if self.round_id and self.player_id:
            if self.round.match_id != self.player.match_id:
                raise ValidationError("Round participant does not belong to this match.")

    def __str__(self):
        return f"{self.player.league_player.player.username} - {self.get_result_display()} ({self.points})"