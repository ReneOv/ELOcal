from rest_framework import viewsets
from elocalBE.league.models import LeaguePlayers
from elocalBE.league.serializers import LeaguePlayersSerializer

class LeaguePlayerViewSet(viewsets.ModelViewSet):
    serializer_class = LeaguePlayersSerializer

    def get_queryset(self):
        return LeaguePlayers.objects.all()