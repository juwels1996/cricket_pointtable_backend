from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, MatchViewSet, points_table
from .views import overall_stats

router = DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'matches', MatchViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/points_table/', points_table),
    path('api/overall_stats/', overall_stats),   # ✅ Make sure this is here
]
