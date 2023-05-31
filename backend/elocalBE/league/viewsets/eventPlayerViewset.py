from rest_framework import viewsets
from elocalBE.league.models import EventPlayers
from elocalBE.league.serializers import EventPlayersSerializer

class LeaguePlayerViewSet(viewsets.ModelViewSet):
    serializer_class = EventPlayersSerializer

    def get_queryset(self):
        return EventPlayers.objects.all()