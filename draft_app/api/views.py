from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Team, Player, Match
from .serializers import TeamSerializer, PlayerSerializer, MatchSerializer
from .serializers import PlayerSerializer
from .models import YouTubeVideo
from .serializers import YouTubeVideoSerializer
from .models import Adviser
from .serializers import AdviserSerializer
# from .models import PDF
# from .serializers import PDFSerializer


class TeamViewSet(viewsets.ModelViewSet):
   queryset = Team.objects.all().order_by('-points', '-net_run_rate')
   serializer_class = TeamSerializer


class PlayerViewSet(viewsets.ModelViewSet):
   queryset = Player.objects.all()
   serializer_class = PlayerSerializer


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all().order_by('date')
    serializer_class = MatchSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class AdviserViewSet(viewsets.ModelViewSet):
    queryset = Adviser.objects.all()
    serializer_class = AdviserSerializer

# class PDFViewSet(viewsets.ModelViewSet):
#     queryset = PDF.objects.all()
#     serializer_class = PDFSerializer




@api_view(['GET'])
def points_table(request):
   teams = Team.objects.all().order_by('-points', '-net_run_rate')
   serializer = TeamSerializer(teams, many=True)
   return Response(serializer.data)


# ✅ **Make sure this function exists in views.py**
@api_view(['GET'])
def overall_stats(request):
    """Retrieve player statistics sorted by most runs"""
    players = Player.objects.all().order_by('-runs')  # Sort by highest runs
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_youtube_videos(request):
    videos = YouTubeVideo.objects.all()
    serializer = YouTubeVideoSerializer(videos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_matches(request):
    status_filter = request.query_params.get('status', None)
    if status_filter:
        matches = Match.objects.filter(status=status_filter)
    else:
        matches = Match.objects.all()
    
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)