from rest_framework import viewsets
from elocalBE.league.models import LeagueEvents
from elocalBE.league.serializers import LeagueEventsSerializer

class LeaguePlayerViewSet(viewsets.ModelViewSet):
    serializer_class = LeagueEventsSerializer

    def get_queryset(self):
        return LeagueEvents.objects.all()