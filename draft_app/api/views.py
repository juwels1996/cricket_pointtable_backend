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
from .serializers import PDFSerializer
from .models import PDF
from .models import Sponsor
from .serializers import SponsorSerializer
from rest_framework import status
from .models import PlayerRegistration
from .serializers import PlayerRegistrationSerializer
from rest_framework.views import APIView
import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse
# from .models import PDF
# from .serializers import PDFSerializer


class TeamViewSet(viewsets.ModelViewSet):
   queryset = Team.objects.all().order_by('-points', '-net_run_rate')
   serializer_class = TeamSerializer


class PlayerViewSet(viewsets.ModelViewSet):
   queryset = Player.objects.all()
   serializer_class = PlayerSerializer


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all().select_related('team1', 'team2', 'winner')  # Fetch related team names
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

class PDFViewSet(viewsets.ModelViewSet):
    queryset = PDF.objects.all()
    serializer_class = PDFSerializer

class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer



@api_view(['GET'])
def points_table(request):
    teams = Team.objects.all()

    # Dynamically calculate net_run_rate for each team
    for team in teams:
        total_runs_scored = team.total_runs_scored
        total_overs_faced = team.total_overs_faced
        total_runs_conceded = team.total_runs_conceded
        total_overs_bowled = team.total_overs_bowled

        # Avoid division by zero
        if total_overs_faced > 0 and total_overs_bowled > 0:
            net_run_rate = (total_runs_scored / total_overs_faced) - (total_runs_conceded / total_overs_bowled)
        else:
            net_run_rate = 0  # Default to 0 if overs are 0

        # Add the calculated NRR to the team instance (temporarily for the response)
        team.net_run_rate = net_run_rate

    # Order the teams by points and NRR (calculated dynamically)
    sorted_teams = sorted(teams, key=lambda t: (t.points, t.net_run_rate), reverse=True)
    serializer = TeamSerializer(sorted_teams, many=True)
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


class PlayerRegistrationView(APIView):
    def post(self, request):
        serializer = PlayerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Player registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# @api_view(['POST'])
# def register_player(request):
#     if request.method == 'POST':
#         # Create the serializer with the incoming data
#         serializer = PlayerRegistrationSerializer(data=request.data)
        
#         # Check if the serializer data is valid
#         if serializer.is_valid():
#             # Save the data and return a success response
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#         # Print the serializer errors for debugging purposes
#         print(f"Error in registration: {serializer.errors}")
        
#         # Handle specific error messages
#         error_messages = []
#         for field, errors in serializer.errors.items():
#             for error in errors:
#                 error_messages.append(f"Error in {field}: {error}")
        
#         # Return the error messages in a readable format
#         return Response(
#             {"detail": error_messages},
#             status=status.HTTP_400_BAD_REQUEST
#         )
    
@api_view(['POST'])
def register_user(request):

    registration_status = PlayerRegistration.objects.first().is_registration_open  # Assuming you have at least one registration object
    
    if not registration_status:
        return JsonResponse({"error": "Registration is closed."}, status=400)
    
    if request.method == 'POST':
        data = request.data.copy()  # Create a mutable copy of the data

        # Check if the player_photo is base64-encoded
        if 'player_photo' in data:
            photo_data = data['player_photo']
            # If it's base64, process it
            if photo_data.startswith('data:image'):
                format, imgstr = photo_data.split(';base64,')  # Get rid of the prefix
                img_data = base64.b64decode(imgstr)  # Decode the base64 image string
                # Create a file-like object from the decoded image data
                player_photo = ContentFile(img_data, name='player_photo.jpg')
                # Replace the player_photo field with the decoded image
                data['player_photo'] = player_photo

        # Create the serializer and validate the data
        serializer = PlayerRegistrationSerializer(data=data)

        if serializer.is_valid():
            # Save the data
            serializer.save()
            # Return the saved data as a response
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return error messages if validation fails
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# @api_view(['GET'])
# def get_player_data(request):
#     players = PlayerRegistration.objects.all()  # Fetch all player data
#     serializer = PlayerRegistrationSerializer(players, many=True)  # Serialize the data
#     return Response(serializer.data) 

@api_view(['GET'])
def get_user_data(request, pk):
    try:
        registration = PlayerRegistration.objects.get(id=pk)  # Get the user by ID
        serializer = PlayerRegistrationSerializer(registration)
        return Response(serializer.data)
    except PlayerRegistration.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

