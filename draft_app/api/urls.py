from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, MatchViewSet, points_table
from .views import overall_stats
from .views import get_youtube_videos
from .views import AdviserViewSet
from .views import PDFViewSet
from .views import OwnerViewSet
from .views import SponsorViewSet
from .views import MatchPhotoGalleryViewSet
from .views import PlayerRegistrationView
from . import views
from django.conf import settings
from django.conf.urls.static import static


# from .views import PDFViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'advisers', AdviserViewSet)
router.register(r'pdfs', PDFViewSet)
router.register(r'sponsor', SponsorViewSet, basename='sponsor')
router.register(r'matchgallery',MatchPhotoGalleryViewSet)
router.register(r'owner',OwnerViewSet)

# router.register(r'pdfs', PDFViewSet)  # Registering PDF viewset

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/points_table/', points_table),
    path('api/overall_stats/', overall_stats),
    path('api/youtube_videos/', get_youtube_videos, name='youtube_videos'),
   path('register_user/', views.register_user, name='register_user'),
    path('get_user_data/<int:pk>/', views.get_user_data, name='get_user_data'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)