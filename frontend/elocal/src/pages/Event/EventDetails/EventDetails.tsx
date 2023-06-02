import React, { useState, useEffect } from "react";
import { Box, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TablePagination, TableRow, Typography } from '@mui/material';
import { useParams } from "react-router-dom";
import { getEvent, getEventPlacements } from "../../../services/event.service";

interface Data {
    name: string;
    placement: number;
}

interface HeadCell {
    disablePadding: boolean;
    id: keyof Data;
    label: string;
    numeric: boolean;
}

const headCells: readonly HeadCell[] = [
    {
        id: 'placement',
        numeric: true,
        disablePadding: false,
        label: '#',
    },
    {
        id: 'name',
        numeric: false,
        disablePadding: false,
        label: 'Player Tag',
    }
];

function PlacementTableHead() {

    return (
        <TableHead>
            <TableRow>
                <TableCell
                    key={'placement'}
                    align="center"
                    sx={{backgroundColor: 'lightblue'}}
                >
                    <strong>#</strong>
                </TableCell>
                <TableCell
                    key={'name'}
                    sx={{backgroundColor: 'lightblue'}}
                >
                    <strong>Player Tag</strong>
                </TableCell>
            </TableRow>
        </TableHead>
    );
} 

export const EventDetails = () => {
    const { eventId } = useParams<{ eventId: string }>();
    const [event, setEvent] = useState<any>();
    const [placements, setPlacements] = useState<any[]>([]);
    const [rows, setRows] = useState<Data[]>([]);
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(16);

    const fetchEvent = async (id: string) => {
        const eventRes = await getEvent(id);
        const placementsRes = await getEventPlacements(id);

        setEvent(eventRes.data);
        setPlacements(placementsRes.data);
    }

    const handleChangePage = (event: unknown, newPage: number) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    const emptyRows =
        page > 0 ? Math.max(0, (1 + page) * rowsPerPage - rows.length) : 0;

    const visibleRows = React.useMemo(
        () =>
            rows.slice(
                page * rowsPerPage,
                page * rowsPerPage + rowsPerPage,
            ),
        [rows, page, rowsPerPage],
    );

    useEffect(() => {
        if (eventId) {
            fetchEvent(eventId);
        }
    }, [eventId]);

    useEffect(() => {
        if (placements.length > 0) {
            setRows(placements.map((entry, index): any => {
                return {
                    name: entry.player.name,
                    placement: entry.placement
                };
            }));
        }
    }, [placements])

    return (
        <Box sx={{ width: '100%', p: 2 }}>
            <Typography variant="h4">
                {event?.tournamentName.replaceAll('-', ' ').toUpperCase()} - {event?.eventName.replaceAll('-', ' ')}
            </Typography>
            <Box sx={{ flexGrow: 1, p: 2}}>
                <Typography sx={{ mt: 1 }}>
                    <strong>Start Date: </strong> {event?.startDate.split('T')[0]}
                </Typography>
                <Typography sx={{ mt: 1 }}>
                    <strong>End Date: </strong> {event?.endDate.split('T')[0]}
                </Typography>
                <Typography sx={{ mt: 1 }}>
                    <strong># of Players: </strong> {event?.players.length}
                </Typography>
            </Box>
            <br/>
            <Typography variant="h5">
                Placements
            </Typography>
            <Box sx={{ p: 1 }}>
                <Paper sx={{ mb: 2, maxWidth: 400 }}>
                    <TableContainer>
                        <Table
                            sx={{ maxWidth: 400 }}
                            aria-labelledby="tableTitle"
                        >
                            <PlacementTableHead/>
                            <TableBody>
                                {visibleRows.map((row, index) => {

                                    return (
                                        <TableRow>
                                            <TableCell align="center">{row.placement}</TableCell>
                                            <TableCell scope="row">{row.name}</TableCell>
                                        </TableRow>
                                    );
                                })}
                                {emptyRows > 0 && (
                                    <TableRow
                                        style={{
                                            height: (53) * emptyRows,
                                        }}
                                    >
                                        <TableCell colSpan={6} />
                                    </TableRow>
                                )}
                            </TableBody>
                        </Table>
                    </TableContainer>
                    <TablePagination
                        rowsPerPageOptions={[8, 16, 24, 32, 64]}
                        component="div"
                        count={rows.length}
                        rowsPerPage={rowsPerPage}
                        page={page}
                        onPageChange={handleChangePage}
                        onRowsPerPageChange={handleChangeRowsPerPage}
                    />
                </Paper>
            </Box>
            
        </Box>
    );
}