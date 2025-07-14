from rest_framework import serializers
from .models import Team, Player, Match, Owner, Coach
from .models import Player
from .models import YouTubeVideo
from .models import Adviser
from .models import PDF
from .models import Sponsor
from .models import PlayerRegistration

class PlayerSerializer(serializers.ModelSerializer):
    team_name = serializers.ReadOnlyField(source="team.name")

    class Meta:
        model = Player
        fields = [
            'id', 'name', 'role', 'image_url', 'category', 'team_name', 'runs', 'matches', 'innings', 
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
    team1_name = serializers.CharField(source='team1.name', read_only=True)
    team2_name = serializers.CharField(source='team2.name', read_only=True)
    winner_name = serializers.SerializerMethodField()  # Use SerializerMethodField for winner_name

    class Meta:
        model = Match
        fields = ['id', 'team1_name', 'team2_name', 'winner_name', 'date', 'time', 'stadium', 
                  'team1_score', 'team1_overs', 'team2_score', 'team2_overs', 'result', 'status']

    def get_winner_name(self, obj):
        # Check if winner exists, if so, return its name, else return None or a default value
        if obj.winner:
            return obj.winner.name
        return None

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
        model = PDF
        fields = ['id', 'title', 'description', 'pdf_link', 'date']

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['name', 'image']

class PlayerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerRegistration
        fields = '__all__'

