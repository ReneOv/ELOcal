import { Box, Button, Card, CardActions, CardContent, Grid, Typography } from "@mui/material";
import React, { useState, useEffect } from "react";
import { getAllLeagues } from "../../../services/league.service";
import { useNavigate } from "react-router-dom";

export const LeagueIndex = () => {
    const [leagues, setLeagues] = useState<any[]>([]);
	const navigate = useNavigate();

    const fetchLeagues = async () => {
        const leaguesRes = await getAllLeagues();
        setLeagues(leaguesRes.data);
    };

    useEffect(() => {
        fetchLeagues();
    }, []);

    return (
        <Box>
            <Typography variant="h4">
                Leagues
            </Typography>
            {/* <Button variant="contained">
                Create New League
            </Button> */}
            <Box sx={{ flexGrow: 1, p: 2}}>
                <Grid container spacing={3} sx={{ flexGrow: 1}}>
                    {leagues.map((league, key) => (
                        <Grid item xs={12} md={6}>
                            <Card variant="outlined">
                                <CardContent>
                                    <Typography variant='h5'>
                                        {league.name}
                                    </Typography>
                                    <Typography sx={{ mt: 1.5 }} color="text.secondary">
                                        # of Events: {league.events.length}
                                    </Typography>
                                    <Typography sx={{ mt: 1.5 }} color="text.secondary">
                                        # of Players: {league.players.length}
                                    </Typography>
                                </CardContent>
                                <CardActions>
                                    <Button size="small" onClick={()=>(navigate(`/leagues/${key + 1}/details`))}>
                                        View Details
                                    </Button>
                                    <Button size="small" onClick={()=>(navigate(`/leagues/${key + 1}/ranking`))}>
                                        View Ranking
                                    </Button>
                                </CardActions>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </Box>
        </Box>
    )
}