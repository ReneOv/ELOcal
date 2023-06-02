import { Box, Button, Card, CardActions, CardContent, Grid, Typography } from "@mui/material";
import React, { useState, useEffect } from "react";
import { getAllEvents } from "../../../services/event.service";
import { useNavigate } from "react-router-dom";

export const EventIndex = () => {
    const [events, setEvents] = useState<any[]>([]);
	const navigate = useNavigate();

    const fetchEvents = async () => {
        const eventRes = await getAllEvents();
        setEvents(eventRes.data)
    };

    useEffect(() => {
        fetchEvents();
    }, []);

    return (
        <Box>
            <Typography variant="h4">
                Events
            </Typography>
            <Box sx={{ flexGrow: 1, p: 2}}>
                <Grid container spacing={3}>
                    {events.map((event, key) => (
                        <Grid item xs={6} md={4}>
                            <Card variant="outlined">
                                <CardContent>
                                    <Typography>
                                        {event.tournamentName.replaceAll('-', ' ').toUpperCase()}
                                    </Typography>
                                    <Typography>
                                        {event.eventName.replaceAll('-', ' ')}
                                    </Typography>
                                    <Typography sx={{ mt: 1.5 }} color="text.secondary">
                                        # of Players: {event.players.length}
                                    </Typography>
                                </CardContent>
                                <CardActions>
                                    <Button size="small" onClick={()=>(navigate(`/events/${key + 1}/details`))}>
                                        View Details
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