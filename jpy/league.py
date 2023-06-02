# Imports
import pysmashgg
import time
import datetime
import csv

from ELOcal import *


# Set start.gg API key
smash = pysmashgg.SmashGG('0607f97f3c95ebcb87a4afc99de7d275')
elo = ELOcal()

# Define csv files
player_csv_columns = ['name', 'eventsAmount', 'eventsTotalScore', 'topsAmount', 'score', "attendanceBoost", "adjustedScore", 'confidenceRating', 'highScore', 'lastEventDate']
player_csv_file = 'players.csv'

event_csv_columns = ['name', 'numEntrants', 'totalScore', 'entrantsIds', 'startDate', 'endDate']
event_csv_file = 'event.csv'

league_text_file = 'league.txt'

# League Info
league_name = 'LCA Chronicles Ranking'
league_startDate = '01/04/2023'
league_endDate = '30/06/2023'

# League Settings
league_minimumEvents = 3
league_eventThreshold = 0.5
league_totalEventScore = 0
league_topThreshold = 8
league_highestEvent = 0
league_participationPercent = 0.2
league_countBo3 = True

# League Ranking Config
league_scoreThreshold = 0
league_scoreAverage = 0
league_scoreMinimum = 0
league_scoreRange = 0

# League Events
league_events = {}
league_eventsIDs = [
    [1, 'lca-sagas-the-final-season-part-1', 'singles'],
    [2, 'lca-bowser-saga-the-middle', 'singles'],
    [3, 'lca-bowser-saga', 'singles'],
    [4, 'los-finos-monthly-2','los-finos-singles'],
    [5, 'lca-roy-saga-the-middle', 'singles'],
    [6, 'lca-roy-saga', 'singles'],
    [7, 'lca-sonic-saga-the-middle', 'singles'],
    [8, 'lca-sonic-saga', 'singles'],
    [9, 'lca-falco-saga-the-middle', 'singles'],
    [10, 'lca-falco-saga', 'singles'],
    [11, 'lca-zelda-saga', 'singles'],
    [12, 'los-finos-monthly-3','los-finos-singles'],
    [13, 'lca-zelda-saga-the-middle', 'singles'],
    [14, 'meteor-fest-2023', 'singles-meteor-fest'],
]

# Assign event IDs to each tournament
for event in league_eventsIDs:
    try:
        eventId = smash.tournament_show_event_id(event[1], event[2])
        event[0] = eventId
    except:
        print('API Error when calling SHOW_EVENTS')
        break

# League Participants
league_participants = {}
e_count = 0

for event in league_eventsIDs:
    e_count+=1
    if e_count % 7 == 0:
        time.sleep(20)
    print('Event ' + str(e_count) + ': ')
    print(event)
    event_metadata = smash.tournament_show_with_brackets(event[1], event[0])
    event_endDate = event_metadata['endTimestamp']
    event_totalScore = 0
    event_entrantsIds = []
    entrants = []
    page = 1

    # Get list of entrants from an event
    while True:
        try:
            entrantsRes = smash.event_show_entrants(event[0], page)
            if len(entrantsRes) == 0:
                break
            else:
                entrants += entrantsRes
                page += 1
        except:
            print('API Error when calling SHOW_ENTRANTS')
            break

    for entrant in entrants:
        # Gets player's global start.gg ID
        playerId = entrant['entrantPlayers'][0]['playerId']
        event_entrantsIds.append(playerId)
        # Checks to see if playered was inside the Top X threshold for league
        playerTop = 1 if entrant['finalPlacement'] <= league_topThreshold else 0

        # If player exists, update their info
        if playerId in league_participants:
            league_participants[playerId]['eventsAmount'] += 1
            league_participants[playerId]['sount'] += playerTop
            league_participants[playerId]['lastEventDate'] = event_endDate

            event_totalScore += league_participants[playerId]['score']
        
        # If player does not exist, add them to database
        else:
            league_participants[playerId] = {
                'name': entrant['entrantPlayers'][0]['playerTag'],
                'eventsAmount': 1,
                'eventsTotalScore': 0,
                'topsAmount': playerTop,
                'score': 1500,
                'confidenceRating': 350,
                'highScore': 0,
                'lastEventDate': event_endDate
            }

            event_totalScore += 1000

    # Save event info into dictionary
    event_totalScore = event_totalScore / 100
    league_events[event[0]] = {
        'name': event[1],
        'numEntrants': len(entrants),
        'totalScore': event_totalScore,
        'entrantsIds': event_entrantsIds,
        'startDate': event_metadata['startTimestamp'],
        'endDate': event_endDate
    }

    print(league_events[event[0]])

    # Update total event score for each participant
    for id in event_entrantsIds:
        league_participants[id]['eventsTotalScore'] += event_totalScore

    # Update league scores
    league_totalEventScore += event_totalScore
    if ((event_totalScore) > league_highestEvent):
        league_highestEvent = event_totalScore

    # Begin calculating score
    sets = []
    dqs = []
    played = []
    page = 1
    k = league_highestEvent
    while True:
        try:
            setsRes = smash.event_show_sets(event[0], page)
            if len(setsRes) == 0:
                break
            else:
                sets += setsRes
                page += 1
        except:
            print('API Error when calling SHOW_SETS')
            break

    for set in sets:
        # Get relevant set info
        setId = set['id']
        p1_id = set['entrant1Players'][0]['playerId']
        p2_id = set['entrant2Players'][0]['playerId']
        p1_score = set['entrant1Score']
        p2_score = set['entrant2Score']

        # Check to see if any players lost due to DQ (Not showing up)
        if p1_score == -1 or p2_score == -1:
            if p1_score == -1 and p1_id not in dqs and p1_id not in played:
                league_participants[p1_id]['eventsTotalScore'] -= event_totalScore
                league_participants[p1_id]['eventsAmount'] -= 1
                dqs.append(p1_id)
            elif p2_score == -1 and p2_id not in dqs and p1_id not in played:
                league_participants[p2_id]['eventsTotalScore'] -= event_totalScore
                league_participants[p2_id]['eventsAmount'] -= 1
                dqs.append(p2_id)
        
        # If no player had DQ, then
        else:
            # Check to see if player played pool matches, then left
            if p1_id in dqs and p1_id not in played:
                league_participants[p1_id]['eventsTotalScore'] += event_totalScore
                league_participants[p1_id]['eventsAmount'] += 1
            if p2_id in dqs and p2_id not in played:
                league_participants[p2_id]['eventsTotalScore'] += event_totalScore
                league_participants[p2_id]['eventsAmount'] += 1

            played.append(p1_id)
            played.append(p2_id)
            # Get each player's ranking
            p1_rating = elo.create_rating(league_participants[p1_id]['score'], league_participants[p1_id]['confidenceRating'], league_participants[p1_id]['lastEventDate'])
            p2_rating = elo.create_rating(league_participants[p2_id]['score'], league_participants[p2_id]['confidenceRating'], league_participants[p2_id]['lastEventDate'])

            # Create series
            p1_series = []
            p2_series = []

            if league_countBo3:
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
            
            p1_rated = elo.rate(p1_rating, p1_series, event_endDate)
            p2_rated = elo.rate(p2_rating, p2_series, event_endDate)

            league_participants[p1_id]['score'] = p1_rated.mu
            league_participants[p1_id]['confidenceRating'] = p1_rated.sigma
        
            league_participants[p2_id]['score'] = p2_rated.mu
            league_participants[p2_id]['confidenceRating'] = p2_rated.sigma

            # Set High-Score
            if p1_rated.mu > league_participants[p1_id]['highScore']:
                league_participants[p1_id]['highScore'] = p1_rated.mu
            if p2_rated.mu > league_participants[p2_id]['highScore']:
                league_participants[p2_id]['highScore'] = p2_rated.mu

# Update league configs
league_scoreAverage = league_totalEventScore / len(league_eventsIDs)

if league_eventThreshold * e_count <= league_minimumEvents:
    league_scoreMinimum = league_scoreAverage
    league_scoreThreshold = league_totalEventScore - league_scoreAverage
elif league_eventThreshold * e_count <= league_minimumEvents * 1.5:
    league_scoreMinimum = league_scoreAverage * (league_minimumEvents / 2)
    league_scoreThreshold = league_totalEventScore - league_scoreAverage
elif league_eventThreshold * e_count <= league_minimumEvents * 2:
    league_scoreMinimum = league_scoreAverage * (league_minimumEvents / 1.33)
    league_scoreThreshold = league_totalEventScore - (league_scoreAverage * 3)
else:
    league_scoreMinimum = league_scoreAverage * league_minimumEvents
    league_scoreThreshold = league_eventThreshold * league_totalEventScore

league_scoreRange = league_scoreThreshold - league_scoreMinimum


# Update adjusted scores
for participant in league_participants:
    

    if league_participants[participant]['eventsTotalScore'] <= league_scoreMinimum:
        p_boost = 0
    else:
        p_difference = league_participants[participant]['eventsTotalScore'] - league_scoreThreshold
        if p_difference > 0:
            p_boost = league_participationPercent
        else: 
            p_boost = league_participationPercent + ((p_difference / league_scoreRange) * league_participationPercent)
    
    p_elo = league_participants[participant]['score'] * ((1 - league_participationPercent) + p_boost)

    league_participants[participant]['adjustedScore'] = p_elo
    league_participants[participant]['attendanceBoost'] = p_boost
    


# Write results
try:
    with open(player_csv_file, 'w', newline='',  encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=player_csv_columns)
        writer.writeheader()
        for key in league_participants:
            writer.writerow(league_participants[key])
except IOError:
    print("I/O error")

try:
    with open(event_csv_file, 'w', newline='',  encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=event_csv_columns)
        writer.writeheader()
        for key in league_events:
            writer.writerow(league_events[key])
except IOError:
    print("I/O error")

try:
    with open(league_text_file, 'w') as f:
        f.write('Name: ' + league_name + '\n')
        f.write('Start Date: ' + league_startDate + '\n')
        f.write('End Date: ' + league_endDate + '\n')
        f.write('Minimum Events: ' + str(league_minimumEvents) + '\n')
        f.write('Event Score Threshold: ' + str(league_eventThreshold) + '\n')
        f.write('League Total Score: ' + str(league_totalEventScore) + '\n')
        f.write('Count Top X: ' + str(league_topThreshold) + '\n')
        f.write('Event with highest score: ' + str(league_highestEvent) + '\n')
        f.write('Count match or games: ' + 'Games' if league_countBo3 else 'Match')
        f.write('Participation affects what %: ' + str(league_participationPercent) + '\n')
        f.write('Event score needed for full boost: ' + str(league_scoreThreshold) + '\n')
        f.write('Average event score: ' + str(league_scoreAverage) + '\n')
        f.write('Equivalent to minimum event participation: ' + str(league_scoreMinimum) + '\n')
        f.write('Score range from 0 - full boost: ' + str(league_scoreRange) + '\n')
except IOError:
    print("I/O error")

print('Done.')