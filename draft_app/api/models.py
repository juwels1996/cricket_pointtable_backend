from django.db import models
from django.utils import timezone

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
    description = models.TextField(blank=True, null=True) 
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

    team1_score = models.IntegerField(null=True, blank=True)
    team1_overs = models.FloatField(default=0.0)
    team2_score = models.IntegerField(null=True, blank=True)
    team2_overs = models.FloatField(default=0.0)

    result = models.CharField(max_length=255, blank=True, default="")
    win_by_runs = models.IntegerField(null=True, blank=True)
    win_by_wickets = models.IntegerField(null=True, blank=True)

    status = models.CharField(
        max_length=20, 
        choices=[('upcoming', 'Upcoming'), ('finished', 'Finished')], 
        default='upcoming'
    )

    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name}"


# class Match(models.Model):
#     team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team1_matches")
#     team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team2_matches")
#     date = models.DateField()
#     time = models.TimeField(null=True, blank=True)
#     stadium = models.CharField(max_length=255, blank=True, default="")
#     winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_matches")
#     team1_score = models.IntegerField(null=True, blank=True)
#     team1_overs = models.FloatField(default=0.0)
#     team2_score = models.IntegerField(null=True, blank=True)
#     team2_overs = models.FloatField(default=0.0)
#     result = models.CharField(max_length=255, blank=True, default="")
#     win_by_runs = models.IntegerField(null=True, blank=True)
#     win_by_wickets = models.IntegerField(null=True, blank=True)
#     status = models.CharField(max_length=20, choices=[('upcoming', 'Upcoming'), ('finished', 'Finished')], default='upcoming')

#     def save(self, *args, **kwargs):

#         # --- Only apply logic when marking a match as finished ---
#         apply_result = False
#         if self.pk:
#             # Existing match → check previous state
#             prev = Match.objects.filter(pk=self.pk).first()
#             if prev and prev.status != "finished" and self.status == "finished":
#                 apply_result = True
#         else:
#             # New match being created and already finished
#             if self.status == "finished":
#                 apply_result = True

#         if apply_result:
#             self.apply_match_result()
        
#         print(apply_result, " - Apply match result logic")

#         super().save(*args, **kwargs)

#     # ---------------- HELPERS ---------------- #

#     def apply_match_result(self):
#         """Apply match result once when match is marked finished."""

#         # Fetch fresh DB copies (VERY IMPORTANT)
#         team1 = Team.objects.select_for_update().get(pk=self.team1_id)
#         team2 = Team.objects.select_for_update().get(pk=self.team2_id)

#         # Handle Winner / Tie
#         if self.winner:
#             print("Winner found:", self.winner)

#             winner = Team.objects.select_for_update().get(pk=self.winner_id)
#             loser = team2 if winner == team1 else team1

#             winner.wins += 1
#             winner.points += 2
#             loser.losses += 1

#             margin = self.win_by_runs or self.win_by_wickets
#             self.result = f"Won by {margin} runs/wickets"

#         else:
#             # Match Tied
#             team1.ties += 1
#             team2.ties += 1
#             team1.points += 1
#             team2.points += 1

#         # Update Stats
#         self.update_team_stats(team1, self.team1_score, self.team1_overs, self.team2_score, self.team2_overs)
#         self.update_team_stats(team2, self.team2_score, self.team2_overs, self.team1_score, self.team1_overs)

#         # Calculate NRR
#         team1.net_run_rate = self.calculate_net_run_rate(team1)
#         team2.net_run_rate = self.calculate_net_run_rate(team2)

#         team1.save()
#         team2.save()


#     def update_team_stats(self, team, runs_scored, overs_faced, runs_conceded, overs_bowled):
#         """Updates runs and overs stats of a team."""
#         team.total_runs_scored += runs_scored or 0
#         team.total_overs_faced += overs_faced or 0
#         team.total_runs_conceded += runs_conceded or 0
#         team.total_overs_bowled += overs_bowled or 0

#     def calculate_net_run_rate(self, team):
#         """Calculate the net run rate for a team."""
#         if team.total_overs_faced > 0 and team.total_overs_bowled > 0:
#             return round(
#                 (team.total_runs_scored / team.total_overs_faced) -
#                 (team.total_runs_conceded / team.total_overs_bowled),
#                 2
#             )
#         return 0

#     def __str__(self):
#         return f"{self.team1.name} vs {self.team2.name}"

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
    CATEGORY_CHOICES = [
        ('media', 'Media Sponsor'),
        ('co', 'Co-sponsor'),
        ('main', 'Main Sponsor'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    position = models.PositiveIntegerField(default=0, db_index=True)
    image = models.ManyToManyField('SponsorImage',related_name="sponsor_related_image", blank=True)

    class Meta:
        ordering = ['category', 'position', 'id']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
    


class SponsorImage(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return f"Image for {self.sponsor.name}"
    

class PDF(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()  # Ensure this field is included
    pdf_link = models.URLField()
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class MatchPhotoGallery(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="match_photos")
    photo = models.ImageField(upload_to='match_photos/')
    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(default=timezone.now)  # The date the photo is taken
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the photo is uploaded

    def __str__(self):
        return f"Photos for match on {self.date} between {self.match.team1.name} and {self.match.team2.name}"

    class Meta:
        ordering = ['-date'] 
    
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
    

class Event(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/')
    date = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} ({self.date})"
    
class TestCheck(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
class AnotherTestModel(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description[:50]  # Return first 50 characters of description
