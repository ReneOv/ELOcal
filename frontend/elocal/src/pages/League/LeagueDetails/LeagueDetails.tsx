import React, { useState, useEffect } from "react";
import { Box, Typography } from '@mui/material';
import { useParams } from "react-router-dom";
import { getLeague } from "../../../services/league.service";


export const LeagueDetails = () => {
    const { leagueId } = useParams<{ leagueId: string }>();
    const [league, setLeague] = useState<any>();

    const fetchLeague = async (id: string) => {
        const leagueRes = await getLeague(id);
        setLeague(leagueRes.data);
    }

    useEffect(() => {
        if (leagueId) {
            fetchLeague(leagueId);
        }
    }, [leagueId]);

    return (
        <Box sx={{ width: '100%', p: 2 }}>
            <Typography variant="h4">
                {league?.name}
            </Typography>
            <Box sx={{ flexGrow: 1, p: 2}}>
                <Typography sx={{ mt: 1 }}>
                    <strong>Start date: </strong> {league?.startDate.split('T')[0]}
                </Typography>
                <Typography sx={{ mt: 1 }}>
                    <strong>End date: </strong> {league?.endDate.split('T')[0]}
                </Typography>
                <Typography sx={{ mt: 1 }}>
                    <strong>Required events to qualify: </strong> {league?.minimumEvents}
                </Typography>
                <Typography sx={{ mt: 1 }}>
                    <strong>Participation boost: </strong> {league?.participationBoostPercent / (1 - league?.participationBoostPercent) * 100}%
                </Typography>
                <Typography sx={{ mt: 1 }}>
                    <strong>Required equivalent to get full boost: </strong> {league?.eventThreshold * 100}% of events
                </Typography>
                <Typography sx={{ mt: 1 }}>
                    <strong>Good placements are: </strong> Top {league?.topThreshold}'s
                </Typography>
                <hr/>
                <Typography sx={{ mt: 1 }}>
                    <strong># of Events: </strong> {league?.events.length}
                </Typography>
                <Typography sx={{ mt: 1 }}>
                    <strong># of Players: </strong> {league?.players.length}
                </Typography>
                <Typography sx={{ mt: 1 }}>
                    <strong>Total event score: </strong> {Math.round(league?.totalEventScore)}
                </Typography>
                <Typography sx={{ mt: 1 }}>
                    <strong>Event with highest score: </strong> {Math.round(league?.highestEvent)}
                </Typography>
                <Typography sx={{ mt: 1 }}>
                    <strong>Average event score: </strong> {Math.round(league?.scoreAverage)}
                </Typography>
            </Box>
            
        </Box>
    );
}