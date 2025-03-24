from rest_framework import serializers
from .models import Team, Player, Match, Owner, Coach
from .models import Player
from .models import YouTubeVideo
from .models import Adviser
from .models import PDF

class PlayerSerializer(serializers.ModelSerializer):
    team_name = serializers.ReadOnlyField(source="team.name")

    class Meta:
        model = Player
        fields = [
            'id', 'name', 'image_url', 'category', 'team_name', 'runs', 'matches', 'innings', 
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
    class Meta:
        model = Match
        fields = ['id', 'team1_name', 'team2_name', 'date', 'team1_score', 'team1_overs', 'team2_score', 'team2_overs', 'result', 'status']

    class Meta:
        model = Match
        fields = '__all__'

class YouTubeVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouTubeVideo
        fields = '__all__'

class AdviserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adviser
        fields = ['id', 'name', 'image_url', 'designation']

class PDFSerializer(serializers.ModelSerializer):
    class Meta:
        model: PDF
        fields = ['id', 'title', 'pdf_link', 'upload_date']
