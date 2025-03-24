from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    logo = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=7, default="#000000")
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

    def __str__(self):
        return self.name


class Owner(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=255, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="owners")

    def __str__(self):
        return self.name


class Coach(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=255, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="coaches")

    def __str__(self):
        return self.name


class Player(models.Model):
    CATEGORY_CHOICES = [
        ('Local', 'Local'),
        ('Semi-Local', 'Semi-Local'),
        ('Overseas', 'Overseas'),
    ]
    ROLE_CHOICES = [
        ('Batsman', 'Batsman'),
        ('Bowler', 'Bowler'),
        ('All-Rounder', 'All-Rounder'),
        ('Wicket-Keeper', 'Wicket-Keeper'),
    ]
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Batsman")
    image_url = models.CharField(max_length=255, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name="players")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Local')  # New field
    runs = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)
    innings = models.IntegerField(default=0)
    not_outs = models.IntegerField(default=0)
    highest_score = models.CharField(max_length=10, default="0")
    average = models.FloatField(default=0.0)
    balls_faced = models.IntegerField(default=0)
    strike_rate = models.FloatField(default=0.0)
    hundreds = models.IntegerField(default=0)
    fifties = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    sixes = models.IntegerField(default=0)

    def calculate_stats(self):
        """Auto-calculate batting average and strike rate."""
        if self.innings - self.not_outs > 0:
            self.average = round(self.runs / (self.innings - self.not_outs), 2)
        else:
            self.average = 0.0

        if self.balls_faced > 0:
            self.strike_rate = round((self.runs / self.balls_faced) * 100, 2)
        else:
            self.strike_rate = 0.0

    def save(self, *args, **kwargs):
        self.calculate_stats()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team1_matches")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team2_matches")
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    stadium = models.CharField(max_length=255, blank=True, default="") 
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_matches")
    team1_score = models.IntegerField(null=True, blank=True)  # Score for team1
    team1_overs = models.FloatField(default=0.0)
    team2_score = models.IntegerField(null=True, blank=True)  # Score for team2
    team2_overs = models.FloatField(default=0.0)
    result = models.CharField(max_length=255, blank=True, default="")

    # New fields to track the winning condition (runs or wickets)
    win_by_runs = models.IntegerField(null=True, blank=True, default=None)  # If a team wins by runs, store the number of runs.
    win_by_wickets = models.IntegerField(null=True, blank=True, default=None)  # If a team wins by wickets, store the number of wickets.

    status = models.CharField(max_length=20, choices=[('upcoming', 'Upcoming'), ('finished', 'Finished')], default='upcoming')

    def save(self, *args, **kwargs):
        if self.status == 'finished':  # Only update winner, loser, and scores if the match is finished
            if self.winner:
                self.winner.wins += 1
                loser = self.team1 if self.winner == self.team2 else self.team2
                loser.losses += 1
                if self.win_by_runs:
                    self.result = f"Won by {self.win_by_runs} runs"
                elif self.win_by_wickets:
                    self.result = f"Won by {self.win_by_wickets} wickets"
            else:
                self.team1.ties += 1
                self.team2.ties += 1

            # Update scores and overs for both teams
            self.team1.total_runs_scored += self.team1_score or 0
            self.team1.total_overs_faced += self.team1_overs
            self.team1.total_runs_conceded += self.team2_score or 0
            self.team1.total_overs_bowled += self.team2_overs

            self.team2.total_runs_scored += self.team2_score or 0
            self.team2.total_overs_faced += self.team2_overs
            self.team2.total_runs_conceded += self.team1_score or 0
            self.team2.total_overs_bowled += self.team1_overs

            self.team1.save()
            self.team2.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name}"


class YouTubeVideo(models.Model):
    title = models.CharField(max_length=255)
    video_link = models.URLField()
    thumbnail_url = models.URLField()  # Thumbnail image URL for carousel
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Adviser(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField()  # URL to the adviser's image
    designation = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class   PDF(models.Model):
    title = models.CharField(max_length=255)
    pdf_link = models.URLField()  # PDF URL link
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title 