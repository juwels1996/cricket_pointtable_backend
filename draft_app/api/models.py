from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    matches_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    ties = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    total_runs_scored = models.IntegerField(default=0)
    total_overs_faced = models.FloatField(default=0.0)
    total_runs_conceded = models.IntegerField(default=0)
    total_overs_bowled = models.FloatField(default=0.0)
    net_run_rate = models.FloatField(default=0.0)

    def calculate_nrr(self):
        if self.total_overs_faced > 0 and self.total_overs_bowled > 0:
            self.net_run_rate = (self.total_runs_scored / self.total_overs_faced) - (self.total_runs_conceded / self.total_overs_bowled)
        else:
            self.net_run_rate = 0.0

    def update_points(self):
        self.points = (self.wins * 2) + (self.ties * 1)

    def save(self, *args, **kwargs):
        self.calculate_nrr()
        self.update_points()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name="players")

    def __str__(self):
        return self.name


class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team1_matches")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team2_matches")
    date = models.DateField()
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    team1_score = models.IntegerField()
    team1_overs = models.FloatField()
    team2_score = models.IntegerField()
    team2_overs = models.FloatField()
    result = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if self.winner:
            self.winner.wins += 1
            loser = self.team1 if self.winner == self.team2 else self.team2
            loser.losses += 1
        else:
            self.team1.ties += 1
            self.team2.ties += 1

        self.team1.matches_played += 1
        self.team2.matches_played += 1

        self.team1.total_runs_scored += self.team1_score
        self.team1.total_overs_faced += self.team1_overs
        self.team1.total_runs_conceded += self.team2_score
        self.team1.total_overs_bowled += self.team2_overs

        self.team2.total_runs_scored += self.team2_score
        self.team2.total_overs_faced += self.team2_overs
        self.team2.total_runs_conceded += self.team1_score
        self.team2.total_overs_bowled += self.team1_overs

        self.team1.save()
        self.team2.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name}"
