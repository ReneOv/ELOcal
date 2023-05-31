from rest_framework import routers
from elocalBE.league.viewsets.leagueViewset import LeagueViewSet
from elocalBE.league.viewsets.playerViewset import PlayerViewSet
from elocalBE.league.viewsets.eventViewset import EventViewSet
from elocalBE.league.viewsets.leaguePlayerViewset import LeaguePlayerViewSet

router = routers.SimpleRouter()
router.register(r'league', LeagueViewSet, basename='league')
router.register(r'player', PlayerViewSet, basename='player')
router.register(r'event', EventViewSet, basename='event')
router.register(r'leaguePlayer', LeaguePlayerViewSet, basename='leaguePlayer')