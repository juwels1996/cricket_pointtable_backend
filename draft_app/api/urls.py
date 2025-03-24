from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, MatchViewSet, points_table
from .views import overall_stats
from .views import get_youtube_videos
from .views import AdviserViewSet
# from .views import PDFViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'advisers', AdviserViewSet)
# router.register(r'pdfs', PDFViewSet)  # Registering PDF viewset

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/points_table/', points_table),
    path('api/overall_stats/', overall_stats),
    path('api/youtube_videos/', get_youtube_videos, name='youtube_videos'),
]
