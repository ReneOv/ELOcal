from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from datetime import datetime
import environ
import pysmashgg

from elocalBE.league.models import Event, Player, EventPlayers
from elocalBE.league.serializers import EventSerializer

env = environ.Env()
environ.Env.read_env()

smash = pysmashgg.SmashGG(env('STARTGG_KEY'))
    
class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.all()
    
    def create(self, request, *args, **kwargs):
        error = False

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        event_tournamentName = data['tournamentName']
        event_eventName = data['eventName']

        # Get event metadata
        try:
            event_eventId = smash.tournament_show_event_id(event_tournamentName, event_eventName)
            metadata = smash.tournament_show_with_brackets(event_tournamentName, event_eventName)
            event_startDate = metadata['startTimestamp']
            event_endDate = metadata['endTimestamp']

            # Initialize custom variables
            entrants = []
            page = 1

            # Get list of entrants from an event
            while True:
                try:
                    entrantsRes = smash.event_show_entrants(event_eventId, page)
                    if len(entrantsRes) == 0:
                        break
                    else:
                        entrants += entrantsRes
                        page += 1
                except Exception as e:
                    print('API Error when calling SHOW_ENTRANTS')
                    print(e)
                    error = True
                    break
            
            data['eventId'] = event_eventId
            data['startDate'] = datetime.fromtimestamp(event_startDate)
            data['endDate'] = datetime.fromtimestamp(event_endDate)
            data['numEntrants'] = len(entrants)

            try:
                save_serializer = self.serializer_class(data=data)
                save_serializer.is_valid(raise_exception=True)

                myEvent = save_serializer.save()

                with transaction.atomic():
                    for player in entrants:
                        # Gets player's global start.gg ID
                        player_playerId = player['entrantPlayers'][0]['playerId']
                        player_name = player['entrantPlayers'][0]['playerTag']
                        try:
                            myPlayer, created = Player.objects.get_or_create(playerId=player_playerId, name=player_name)
                            event_player = EventPlayers(event = myEvent, player = myPlayer, placement=player['finalPlacement'])
                            event_player.save()
                        except Exception as e:
                            print('Error when saving player in event')
                            print(e)
                            error = True

            except Exception as e:
                print('Error when saving event with serializer')
                print(e)
                error = True

        except Exception as e:
            print('API Error when calling SHOW_EVENT_ID / SHOW_WITH_BRACKETS')
            print(e)
            error = True
        

        if error:
            return Response(status=400)
        else:
            return Response(status=status.HTTP_201_CREATED)