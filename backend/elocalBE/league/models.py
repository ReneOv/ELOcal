from django.db import models
from django.conf import settings

class Player(models.Model):
    playerId = models.IntegerField(unique=True, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Event(models.Model):
    eventId = models.IntegerField()
    tournamentName = models.CharField(max_length=255)
    eventName = models.CharField(max_length=255)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    numEntrants = models.IntegerField()

    players = models.ManyToManyField(Player, through='EventPlayers', blank=True)

    def __str__(self):
        return "{}_{}".format(self.tournamentName, self.eventName)


class League(models.Model):
    name = models.CharField(max_length=255)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    minimumEvents = models.IntegerField()
    eventThreshold = models.FloatField()
    topThreshold = models.IntegerField()
    totalEventScore = models.FloatField(default=0)
    highestEvent = models.FloatField(default=0)
    participationBoostPercent = models.FloatField()
    countBo3 = models.BooleanField()
    scoreThreshold = models.FloatField(default=0)
    scoreAverage = models.FloatField(default=0)
    scoreMinimum = models.FloatField(default=0)
    scoreRange = models.FloatField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    players = models.ManyToManyField(Player, through='LeaguePlayers', blank=True)
    events = models.ManyToManyField(Event, through='LeagueEvents', blank=True)

    def __str__(self):
        return self.name


class LeaguePlayers(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    events = models.IntegerField(default=0)
    tops = models.IntegerField(default=0)
    score = models.FloatField(default=1500)
    adjustedScore = models.FloatField(default=0)
    highScore = models.FloatField(default=0)
    qualifiedScore = models.FloatField(default=0)
    tier = models.CharField(max_length=255)
    attendanceBoost = models.FloatField(default=0)
    eventsTotalScore = models.FloatField(default=0)
    confidenceRating = models.FloatField(default=0)
    lastEventDate = models.DateTimeField()

    def __str__(self):
        return "{}_{}".format(self.player.__str__(), self.league.__str__())
    

class LeagueEvents(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    totalScore = models.FloatField()

    def __str__(self):
        return "{}_{}".format(self.event.__str__(), self.league.__str__())
    

class EventPlayers(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    placement = models.IntegerField()

    def __str__(self):
        return "{}_{}".format(self.player.__str__(), self.event.__str__())
