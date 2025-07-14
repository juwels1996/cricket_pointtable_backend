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
    win_by_runs = models.IntegerField(null=True, blank=True, default=None)
    win_by_wickets = models.IntegerField(null=True, blank=True, default=None)
    status = models.CharField(max_length=20, choices=[('upcoming', 'Upcoming'), ('finished', 'Finished')], default='upcoming')

    def save(self, *args, **kwargs):
        if self.status == 'finished':  # Only update when the match is finished
            if self.winner:
                # Update wins, losses, and points
                self.winner.wins += 1
                loser = self.team1 if self.winner == self.team2 else self.team2
                loser.losses += 1
                self.winner.points += 2  # Winner gets 2 points
                self.result = f"Won by {self.win_by_runs if self.win_by_runs else self.win_by_wickets} runs/wickets"
            else:
                # It's a tie
                self.team1.ties += 1
                self.team2.ties += 1
                self.team1.points += 1
                self.team2.points += 1

            # Update runs and overs for both teams
            self.team1.total_runs_scored += self.team1_score or 0
            self.team1.total_overs_faced += self.team1_overs
            self.team1.total_runs_conceded += self.team2_score or 0
            self.team1.total_overs_bowled += self.team2_overs

            self.team2.total_runs_scored += self.team2_score or 0
            self.team2.total_overs_faced += self.team2_overs
            self.team2.total_runs_conceded += self.team1_score or 0
            self.team2.total_overs_bowled += self.team1_overs

            # Recalculate net run rate
            self.team1.net_run_rate = self.calculate_net_run_rate(self.team1)
            self.team2.net_run_rate = self.calculate_net_run_rate(self.team2)

            # Save the updated team data
            self.team1.save()
            self.team2.save()

        super().save(*args, **kwargs)

    def calculate_net_run_rate(self, team):
        """Calculate the net run rate for a team."""
        if team.total_overs_faced > 0 and team.total_overs_bowled > 0:
            nrr = (team.total_runs_scored / team.total_overs_faced) - (team.total_runs_conceded / team.total_overs_bowled)
            return round(nrr, 2)
        return 0

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
    
class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='banners/')
    

class PDF(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()  # Ensure this field is included
    pdf_link = models.URLField()
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class PlayerRegistration(models.Model):
    AREA_CHOICES = [
        ('Local', 'Local'),
        ('Semi-Local', 'Semi-Local'),
        ('Overseas', 'Overseas'),
    ]
    SPECIALITY_CHOICES = [
        ('Batsman', 'Batsman'),
        ('Bowler', 'Bowler'),
        ('All-Rounder', 'All-Rounder'),
    ]
    CATEGORY_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]

    bkash_number = models.CharField(max_length=20, null=True, blank=True)
    bkash_transaction_id = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    district = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    nid_or_birth_certificate_no = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    area = models.CharField(max_length=20, choices=AREA_CHOICES)
    speciality = models.CharField(max_length=20, choices=SPECIALITY_CHOICES)
    player_category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    player_photo = models.ImageField(upload_to='player_photos/', null=True, blank=True)
    is_registration_open = models.BooleanField(default=True)

    def __str__(self):
        return self.name
