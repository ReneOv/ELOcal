# Generated by Django 4.2.1 on 2023-05-30 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventId', models.IntegerField(editable=False, unique=True)),
                ('tournamentName', models.CharField(max_length=255)),
                ('eventName', models.CharField(max_length=255)),
                ('startDate', models.DateTimeField()),
                ('endDate', models.DateTimeField()),
                ('numEntrants', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('startDate', models.DateTimeField()),
                ('endDate', models.DateTimeField()),
                ('minimumEvents', models.IntegerField()),
                ('eventThreshold', models.FloatField()),
                ('topThreshold', models.IntegerField()),
                ('totalEventScore', models.FloatField(default=0)),
                ('highestEvent', models.FloatField(default=0)),
                ('participationBoostPercent', models.FloatField()),
                ('countBo3', models.BooleanField()),
                ('scoreThreshold', models.FloatField(default=0)),
                ('scoreAverage', models.FloatField(default=0)),
                ('scoreMinimum', models.FloatField(default=0)),
                ('scoreRange', models.FloatField(default=0)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playerId', models.IntegerField(editable=False, unique=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='LeaguePlayers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('events', models.IntegerField(default=0)),
                ('tops', models.IntegerField(default=0)),
                ('score', models.FloatField(default=1500)),
                ('adjustedScore', models.FloatField(default=0)),
                ('highScore', models.FloatField(default=0)),
                ('attendanceBoost', models.FloatField(default=0)),
                ('eventsTotalScore', models.FloatField(default=0)),
                ('confidenceRating', models.FloatField(default=0)),
                ('lastEventDate', models.DateTimeField()),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.league')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.player')),
            ],
        ),
        migrations.CreateModel(
            name='LeagueEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalScore', models.FloatField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.event')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.league')),
            ],
        ),
        migrations.AddField(
            model_name='league',
            name='events',
            field=models.ManyToManyField(blank=True, through='league.LeagueEvents', to='league.event'),
        ),
        migrations.AddField(
            model_name='league',
            name='players',
            field=models.ManyToManyField(blank=True, through='league.LeaguePlayers', to='league.player'),
        ),
        migrations.CreateModel(
            name='EventPlayers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placement', models.IntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.event')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.player')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='players',
            field=models.ManyToManyField(blank=True, through='league.EventPlayers', to='league.player'),
        ),
    ]
