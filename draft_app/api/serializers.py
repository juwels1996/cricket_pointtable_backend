from rest_framework import serializers
from .models import Team, Player, Match

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)

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
