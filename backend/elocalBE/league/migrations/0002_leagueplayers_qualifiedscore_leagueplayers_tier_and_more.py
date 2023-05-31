# Generated by Django 4.2.1 on 2023-05-31 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leagueplayers',
            name='qualifiedScore',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='leagueplayers',
            name='tier',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='event',
            name='eventId',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='leagueevents',
            name='totalScore',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='leagueplayers',
            name='lastEventDate',
            field=models.DateTimeField(null=True),
        ),
    ]
