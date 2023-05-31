from rest_framework import serializers
from elocalBE.league.models import League, Player, Event, LeaguePlayers, LeagueEvents, EventPlayers

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            'playerId',
            'name'
        ]

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'eventId',
            'tournamentName',
            'eventName',
            'startDate',
            'endDate',
            'numEntrants',
            'players'
        ]

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = [
            'name',
            'startDate',
            'endDate',
            'minimumEvents',
            'eventThreshold',
            'topThreshold',
            'participationBoostPercent',
            'countBo3',
            'totalEventScore',
            'highestEvent',
            'scoreThreshold',
            'scoreAverage',
            'scoreMinimum',
            'scoreRange',
            'createdAt',
            'updatedAt',
            'admin',
            'players',
            'events'
        ]

class LeaguePlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaguePlayers
        depth = 1
        fields = [
            'league',
            'player',
            'events',
            'tops',
            'score',
            'adjustedScore',
            'highScore',
            'qualifiedScore',
            'tier',
            'attendanceBoost',
            'eventsTotalScore',
            'confidenceRating',
            'lastEventDate',
        ]

class LeagueEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeagueEvents
        depth = 1
        fields = [
            'league',
            'event',
            'totalScore'
        ]

class EventPlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPlayers
        depth = 1
        fields = [
            'event',
            'player',
            'placement'
        ]