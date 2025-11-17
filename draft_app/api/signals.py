from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Match, Team

@receiver(post_save, sender=Match)
def update_team_stats_after_match(sender, instance, created, **kwargs):
    if not created or instance.status != "finished":
        return

    team1 = instance.team1
    team2 = instance.team2

    # Increment matches played
    team1.matches_played += 1
    team2.matches_played += 1

    # Winner / Loser logic
    if instance.winner:
        winner = instance.winner
        if winner == team1:
            team1.wins += 1
            team2.losses += 1
            team1.points += 2
        else:
            team2.wins += 1
            team1.losses += 1
            team2.points += 2
    else:
        # Tie
        team1.ties += 1
        team2.ties += 1
        team1.points += 1
        team2.points += 1

    # Update runs & overs
    team1.total_runs_scored += instance.team1_score or 0
    team1.total_overs_faced += instance.team1_overs or 0
    team1.total_runs_conceded += instance.team2_score or 0
    team1.total_overs_bowled += instance.team2_overs or 0

    team2.total_runs_scored += instance.team2_score or 0
    team2.total_overs_faced += instance.team2_overs or 0
    team2.total_runs_conceded += instance.team1_score or 0
    team2.total_overs_bowled += instance.team1_overs or 0

    # Calculate NRR
    team1.net_run_rate = calculate_nrr(team1)
    team2.net_run_rate = calculate_nrr(team2)

    # Save all changes at once
    team1.save()
    team2.save()


def calculate_nrr(team):
    if team.total_overs_faced > 0 and team.total_overs_bowled > 0:
        return round(
            (team.total_runs_scored / team.total_overs_faced) -
            (team.total_runs_conceded / team.total_overs_bowled),
            2
        )
    return 0
