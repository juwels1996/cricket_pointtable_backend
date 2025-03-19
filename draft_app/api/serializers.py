from rest_framework import serializers
from .models import Team, Player, Match, Owner, Coach
from .models import Player


class PlayerSerializer(serializers.ModelSerializer):
    team_name = serializers.ReadOnlyField(source="team.name")

    class Meta:
        model = Player
        fields = [
            'id', 'name', 'image_url', 'team_name', 'runs', 'matches', 'innings', 
            'not_outs', 'highest_score', 'average', 'balls_faced', 'strike_rate',
            'hundreds', 'fifties', 'fours', 'sixes'
        ]

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'

class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    owners = OwnerSerializer(many=True, read_only=True)
    coaches = CoachSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    team1_name = serializers.ReadOnlyField(source="team1.name")
    team2_name = serializers.ReadOnlyField(source="team2.name")
    winner_name = serializers.ReadOnlyField(source="winner.name")

    class Meta:
        model = Match
        fields = '__all__'
