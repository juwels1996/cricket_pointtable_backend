from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Team, Player, Match
from .serializers import TeamSerializer, PlayerSerializer, MatchSerializer
from .serializers import PlayerSerializer


class TeamViewSet(viewsets.ModelViewSet):
   queryset = Team.objects.all().order_by('-points', '-net_run_rate')
   serializer_class = TeamSerializer


class PlayerViewSet(viewsets.ModelViewSet):
   queryset = Player.objects.all()
   serializer_class = PlayerSerializer


class MatchViewSet(viewsets.ModelViewSet):
   queryset = Match.objects.all()
   serializer_class = MatchSerializer


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