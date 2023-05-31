from rest_framework import viewsets
from rest_framework.decorators import action
from elocalBE.league.models import League
from elocalBE.league.serializers import LeagueSerializer

class LeagueViewSet(viewsets.ModelViewSet):
    serializer_class = LeagueSerializer

    def get_queryset(self):
        return League.objects.all()
