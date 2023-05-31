from rest_framework import viewsets
from elocalBE.league.models import Player
from elocalBE.league.serializers import PlayerSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer

    def get_queryset(self):
        return Player.objects.all()