from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
import pysmashgg
import environ
from rest_framework.decorators import action
from datetime import datetime as dt
from elocalBE.league.models import League, Event, LeagueEvents, LeaguePlayers, EventPlayers
from elocalBE.league.serializers import LeagueSerializer, PlayerSerializer, LeaguePlayersSerializer
from elocalBE.elocalAlgorithm.ELOcal import *

env = environ.Env()
environ.Env.read_env()
smash = pysmashgg.SmashGG(env('STARTGG_KEY'))
elo = ELOcal()

class LeagueViewSet(viewsets.ModelViewSet):
    serializer_class = LeagueSerializer

    def get_queryset(self):
        return League.objects.all()
    
    @action(detail=True, methods=['post'])
    def add_event(self, request, pk):
        error = False
        data = request.data
        league_obj = self.get_object()
        event_obj = Event.objects.get(pk=data['event_id'])

        try:
            with transaction.atomic():
                if LeagueEvents.objects.filter(event = event_obj, league = league_obj).exists():
                    raise Exception('Event previously added to league')
                else:
                    league_event = LeagueEvents(event = event_obj, league = league_obj)
                    league_event.save()

                    for player in event_obj.players.all():
                        if LeaguePlayers.objects.filter(player = player, league = league_obj).exists():
                            pass
                        else:
                            league_player = LeaguePlayers(player = player, league = league_obj)
                            league_player.save()

        except Exception as e:
            error = True
            print('Error at add_event to league')
            print(e)
        
        if error:
            return Response(status=400)
        else:
            return Response(status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def get_ranking(self, request, pk):
        error = False
        league_obj = self.get_object()
        players = LeaguePlayers.objects.filter(league=league_obj).all()
        serializer = LeaguePlayersSerializer(players, many=True)

        return Response(serializer.data)
    

    # The chonky function. Runs all the calculations
    @action(detail=True, methods=['post'])
    def update_ranking(self, request, pk):
        error = False
        print('Update began')

        try:
            with transaction.atomic():

                # Get league object and events registered in the league
                league_obj = self.get_object()
                league_totalEventScore = 0
                events = league_obj.events.all().order_by('startDate')
                players = league_obj.players.all()

                # Restart league object
                league_obj.highestEvent = 0
                league_obj.totalEventScore = 0
                league_obj.scoreThreshold = 0
                league_obj.scoreAverage = 0
                league_obj.scoreMinimum = 0
                league_obj.scoreRange = 0
                league_obj.save()

                # Restart player objects
                for player in players:
                    leaguePlayer = LeaguePlayers.objects.filter(league=league_obj, player=player).first()
                    leaguePlayer.events = 0
                    leaguePlayer.tops = 0
                    leaguePlayer.score = 1500
                    leaguePlayer.adjustedScore = 0
                    leaguePlayer.highScore = 0
                    leaguePlayer.qualifiedScore = 0
                    leaguePlayer.attendanceBoost = 0
                    leaguePlayer.eventsTotalScore = 0
                    leaguePlayer.confidenceRating = 350
                    leaguePlayer.lastEventDate = None
                    leaguePlayer.save()

                for event in events:
                    event_totalScore = 0
                    players = event.players.all()

                    for player in players:
                        eventPlayer = EventPlayers.objects.filter(event=event, player=player).first()
                        playerTop = 1 if eventPlayer.placement <= league_obj.topThreshold else 0

                        # Update a League-Player's information
                        leaguePlayer = LeaguePlayers.objects.filter(league=league_obj, player=player).first()
                        leaguePlayer.events += 1
                        leaguePlayer.tops += playerTop
                        leaguePlayer.save()

                        # If player is new, add 1000 to event score instead of 1500
                        if leaguePlayer.score == 1500:
                            event_totalScore += 1000
                        else:
                            event_totalScore += leaguePlayer.score
                    
                    # Update League-Event score for that event
                    leagueEvent = LeagueEvents.objects.filter(league=league_obj, event=event).first()
                    leagueEvent.totalScore = event_totalScore / 100.0
                    leagueEvent.save()

                    for player in players:
                        # Add the event's score to each player that attended
                        leaguePlayer = LeaguePlayers.objects.filter(league=league_obj, player=player).first()
                        leaguePlayer.eventsTotalScore += event_totalScore / 100
                        leaguePlayer.save()

                    # Upate league's event scores
                    league_totalEventScore += event_totalScore
                    if (event_totalScore / 100 > league_obj.highestEvent):
                        league_obj.highestEvent = event_totalScore / 100
                        league_obj.save()
                    

                    # Begin ELOcal calculation
                    sets = []
                    dqs = []
                    played = []
                    page = 1

                    # Fetch event set data
                    while True:
                        try:
                            setsRes = smash.event_show_sets(event.eventId, page)
                            if len(setsRes) == 0:
                                break
                            else:
                                sets += setsRes
                                page += 1
                        except Exception as e:
                            error = True
                            print('API Error when calling SHOW_SETS')
                            print(e)
                            break
                    
                    # Begin running through sets
                    for set in sets:
                        # Get relevant set info
                        p1_id = set['entrant1Players'][0]['playerId']
                        p2_id = set['entrant2Players'][0]['playerId']
                        p1_score = set['entrant1Score']
                        p2_score = set['entrant2Score']
                        
                        p1_leaguePlayer = LeaguePlayers.objects.filter(player__playerId=p1_id).first()
                        p2_leaguePlayer = LeaguePlayers.objects.filter(player__playerId=p2_id).first()

                        # Check to see if any players lost due to DQ (Not showing up)
                        if p1_score == -1 or p2_score == -1:
                            if p1_score == -1 and p1_id not in dqs and p1_id not in played:
                                p1_leaguePlayer.eventsTotalScore -= event_totalScore
                                p1_leaguePlayer.events -= 1
                                dqs.append(p1_id)
                            elif p2_score == -1 and p2_id not in dqs and p1_id not in played:
                                p2_leaguePlayer.eventsTotalScore -= event_totalScore
                                p2_leaguePlayer.events -= 1
                                dqs.append(p2_id)

                        # If no player DQ'd, then
                        else:
                            # Check to see if player played pool matches, then left
                            if p1_id in dqs and p1_id not in played:
                                p1_leaguePlayer.eventsTotalScore += event_totalScore
                                p1_leaguePlayer.events += 1
                            if p2_id in dqs and p2_id not in played:
                                p2_leaguePlayer.eventsTotalScore += event_totalScore
                                p2_leaguePlayer.events += 1

                            played.append(p1_id)
                            played.append(p2_id)

                            # Get each player's ranking
                            p1_rating = elo.create_rating(p1_leaguePlayer.score, p1_leaguePlayer.confidenceRating, p1_leaguePlayer.lastEventDate)
                            p2_rating = elo.create_rating(p2_leaguePlayer.score, p2_leaguePlayer.confidenceRating, p2_leaguePlayer.lastEventDate)

                            # Create series
                            p1_series = []
                            p2_series = []

                            if league_obj.countBo3:
                                # If games are counted

                                # If match ended in a draww
                                if p1_score == p2_score:
                                    p1_series.append((0.5, p2_rating))
                                    p2_series.append((0.5, p1_rating))
                                

                                # If Player 1 won, Player 2's wins are placed first.
                                elif p1_score > p2_score:
                                    for i in range(p2_score):
                                        p1_series.append((0, p2_rating))
                                        p2_series.append((1, p1_rating))
                                    for i in range(p1_score):
                                        p1_series.append((1, p2_rating))
                                        p2_series.append((0, p1_rating))

                                # If Player 2 won, Player 1's wins are placed first.
                                else:
                                    for i in range(p1_score):
                                        p1_series.append((1, p2_rating))
                                        p2_series.append((0, p1_rating))
                                    for i in range(p1_score):
                                        p1_series.append((0, p2_rating))
                                        p2_series.append((1, p1_rating))
                            
                            else:
                                # If false, then only count match result
                                if p1_score > p2_score:
                                    p1_series.append((1, p2_rating))
                                    p2_series.append((0, p1_rating))
                                elif p1_score < p2_score:
                                    p1_series.append((0, p2_rating))
                                    p2_series.append((1, p1_rating))
                                else:
                                    p1_series.append((0.5, p2_rating))
                                    p2_series.append((0.5, p1_rating))
                            
                            # Calculate final changes to rating
                            p1_rated = elo.rate(p1_rating, p1_series, event.endDate)
                            p2_rated = elo.rate(p2_rating, p2_series, event.endDate)

                            # Save updated rating values
                            p1_leaguePlayer.score = p1_rated.mu
                            p1_leaguePlayer.confidenceRating = p1_rated.sigma
                            p1_leaguePlayer.lastEventDate = event.endDate
                        
                            p2_leaguePlayer.score = p2_rated.mu
                            p2_leaguePlayer.confidenceRating = p2_rated.sigma
                            p2_leaguePlayer.lastEventDate = event.endDate

                            # If player has played minimum events, save their initial qualifying score, and begin storing high scores
                            if p1_leaguePlayer.events == league_obj.minimumEvents:
                                p1_leaguePlayer.qualifiedScore = p1_rated.mu
                                p1_leaguePlayer.highScore = p1_rated.mu
                            elif p1_leaguePlayer.events > league_obj.minimumEvents and p1_rated.mu > p1_leaguePlayer.highScore:
                                p1_leaguePlayer.highScore = p1_rated.mu
                            
                            if p2_leaguePlayer.events == league_obj.minimumEvents:
                                p2_leaguePlayer.qualifiedScore = p2_rated.mu
                                p2_leaguePlayer.highScore = p2_rated.mu
                            elif p2_leaguePlayer.events > league_obj.minimumEvents and p2_rated.mu > p2_leaguePlayer.highScore:
                                p2_leaguePlayer.highScore = p2_rated.mu
                            
                            p1_leaguePlayer.save()
                            p2_leaguePlayer.save()

                
                # Update league configs
                league_obj.totalEventScore = league_totalEventScore / 100
                league_obj.scoreAverage = league_obj.totalEventScore / len(events)

                if league_obj.eventThreshold * len(events) <= league_obj.minimumEvents:
                    league_obj.scoreMinimum = league_obj.scoreAverage
                    league_obj.scoreThreshold = league_obj.totalEventScore - league_obj.scoreAverage

                elif league_obj.eventThreshold * len(events) <= league_obj.minimumEvents * 1.5:
                    league_obj.scoreMinimum = league_obj.scoreAverage * (league_obj.minimumEvents / 2)
                    league_obj.scoreThreshold = league_obj.totalEventScore - league_obj.scoreAverage

                elif league_obj.eventThreshold * len(events) <= league_obj.minimumEvents * 2:
                    league_obj.scoreMinimum = league_obj.scoreAverage * (league_obj.minimumEvents / 1.33)
                    league_obj.scoreThreshold = league_obj.totalEventScore - (league_obj.scoreAverage * 3)

                else:
                    league_obj.scoreMinimum = league_obj.scoreAverage * league_obj.minimumEvents
                    league_obj.scoreThreshold = league_obj.eventThreshold * league_obj.totalEventScore

                league_obj.scoreRange = league_obj.scoreThreshold - league_obj.scoreMinimum

                league_obj.save()


                # Update adjusted scores
                for player in players:
                    leaguePlayer = LeaguePlayers.objects.filter(league=league_obj, player=player).first()

                    if leaguePlayer.eventsTotalScore <= league_obj.scoreMinimum:
                        p_boost = 0
                    else:
                        p_difference = leaguePlayer.eventsTotalScore - league_obj.scoreThreshold
                        if p_difference > 0:
                            p_boost = league_obj.participationBoostPercent
                        else: 
                            p_boost = league_obj.participationBoostPercent + ((p_difference / league_obj.scoreRange) * league_obj.participationBoostPercent)
                    
                    p_elo = leaguePlayer.score * ((1 - league_obj.participationBoostPercent) + p_boost)

                    leaguePlayer.adjustedScore = p_elo
                    leaguePlayer.attendanceBoost = p_boost

                    leaguePlayer.save()

        except Exception as e:
            error = True
            print('Error at add_event to league')
            print(e)

        if error:
            return Response(status=400)
        else:
            return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def update_player_ranking(self, request, pk):
        error = False

         # Get league object and its players
        league_obj = self.get_object()
        players = league_obj.players.all()

        try:
            with transaction.atomic():
                for player in players:
                    leaguePlayer = LeaguePlayers.objects.filter(league=league_obj, player=player).first()

                    if leaguePlayer.eventsTotalScore <= league_obj.scoreMinimum:
                        p_boost = 0
                    else:
                        p_difference = leaguePlayer.eventsTotalScore - league_obj.scoreThreshold
                        if p_difference > 0:
                            p_boost = league_obj.participationBoostPercent
                        else: 
                            p_boost = league_obj.participationBoostPercent + ((p_difference / league_obj.scoreRange) * league_obj.participationBoostPercent)
                    
                    p_elo = leaguePlayer.score * ((1 - league_obj.participationBoostPercent) + p_boost)

                    leaguePlayer.adjustedScore = p_elo
                    leaguePlayer.attendanceBoost = p_boost

                    leaguePlayer.save()
                
        except Exception as e:
            error = True
            print('Error at update_player_ranking')
            print(e)

        if error:
            return Response(status=400)
        else:
            return Response(status=status.HTTP_201_CREATED)