from rest_framework import serializers
from .models import Team, Player, Match, Owner, Coach
from .models import Player
from .models import YouTubeVideo
from .models import Adviser
from .models import PDF
from .models import Event
from .models import Sponsor
from .models import PlayerRegistration
from .models import MatchPhotoGallery

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

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'

class PDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDF
        fields = ['id', 'title', 'description', 'pdf_link', 'date']

class SponsorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.SerializerMethodField()
    category_label = serializers.SerializerMethodField()

    class Meta:
        model = Sponsor
        fields = ['id', 'name', 'image', 'category', 'category_label', 'position']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            url = obj.image.url
            # Build absolute URL (https-safe for your frontend)
            if request is not None:
                return request.build_absolute_uri(url).replace('http://', 'https://')
            return url
        return None

    def get_category_label(self, obj):
        return dict(Sponsor.CATEGORY_CHOICES).get(obj.category, obj.category)

class PlayerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerRegistration
        fields = '__all__'


class MatchPhotoGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchPhotoGallery
        fields = ['id', 'match', 'photo', 'description', 'date', 'uploaded_at']
        read_only_fields = ['uploaded_at']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'image', 'date'] 

