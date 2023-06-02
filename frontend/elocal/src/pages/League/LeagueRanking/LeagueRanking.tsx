import React, { useState, useEffect } from "react";
import { Box, TablePagination, TableSortLabel, Typography } from '@mui/material';
import { useParams } from "react-router-dom";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { visuallyHidden } from '@mui/utils';
import { getLeagueRanking } from "../../../services/league.service";

type Order = 'asc' | 'desc';

interface Data {
    name: string;
    events: number;
    tops: number;
    adjustedScore: number;
    highScore: number;
    score: number;
    tier: string;
}

interface HeadCell {
    disablePadding: boolean;
    id: keyof Data;
    label: string;
    numeric: boolean;
}

interface RankingTableProps {
    onRequestSort: (event: React.MouseEvent<unknown>, property: keyof Data) => void;
    order: Order;
    orderBy: string;
    rowCount: number;
}

function descendingComparator<T>(a: T, b: T, orderBy: keyof T) {
    if (b[orderBy] < a[orderBy]) {
        return -1;
    }
    if (b[orderBy] > a[orderBy]) {
        return 1;
    }
    return 0;
}

function getComparator<Key extends keyof any>(
    order: Order,
    orderBy: Key,
): (
    a: { [key in Key]: number | string },
    b: { [key in Key]: number | string },
) => number {
    return order === 'desc'
        ? (a, b) => descendingComparator(a, b, orderBy)
        : (a, b) => -descendingComparator(a, b, orderBy);
}

function stableSort<T>(array: readonly T[], comparator: (a: T, b: T) => number) {
    const stabilizedThis = array.map((el, index) => [el, index] as [T, number]);
    stabilizedThis.sort((a, b) => {
        const order = comparator(a[0], b[0]);
        if (order !== 0) {
            return order;
        }
        return a[1] - b[1];
    });
    return stabilizedThis.map((el) => el[0]);
}

const headCells: readonly HeadCell[] = [
    {
        id: 'name',
        numeric: false,
        disablePadding: false,
        label: 'Tag',
    },
    {
        id: 'events',
        numeric: true,
        disablePadding: false,
        label: 'Eventos',
    },
    {
        id: 'tops',
        numeric: true,
        disablePadding: false,
        label: 'Top 8\'s',
    },
    {
        id: 'adjustedScore',
        numeric: true,
        disablePadding: false,
        label: 'Score',
    },
    {
        id: 'highScore',
        numeric: true,
        disablePadding: false,
        label: 'High-Score',
    },
    {
        id: 'tier',
        numeric: false,
        disablePadding: false,
        label: 'Tier',
    },
    {
        id: 'score',
        numeric: true,
        disablePadding: false,
        label: 'Glicko',
    },
];

function RankingTableHead(props: RankingTableProps) {
    const { order, orderBy, rowCount, onRequestSort } =
        props;
    const createSortHandler =
        (property: keyof Data) => (event: React.MouseEvent<unknown>) => {
            onRequestSort(event, property);
        };
    let counter = 0;

    return (
        <TableHead>
            <TableRow>
                <TableCell
                        key={'num'}
                        sx={{backgroundColor: 'lightblue'}}
                    >
                        <strong>#</strong>
                    </TableCell>
                {headCells.map((headCell) => (
                    <TableCell
                        key={headCell.id}
                        align={headCell.numeric ? 'left' : 'left'}
                        padding={headCell.disablePadding ? 'none' : 'normal'}
                        sortDirection={orderBy === headCell.id ? order : false}
                        sx={{backgroundColor: 'lightblue'}}
                    >
                        <TableSortLabel
                            active={orderBy === headCell.id}
                            direction={orderBy === headCell.id ? order : 'asc'}
                            onClick={createSortHandler(headCell.id)}
                        >
                            <strong>{headCell.label}</strong>
                            {orderBy === headCell.id ? (
                                <Box component="span" sx={visuallyHidden}>
                                    {order === 'desc' ? 'sorted descending' : 'sorted ascending'}
                                </Box>
                            ) : null}
                        </TableSortLabel>
                    </TableCell>
                ))}
            </TableRow>
        </TableHead>
    );
}

export const LeagueRanking = () => {
    const { leagueId } = useParams<{ leagueId: string }>();
    const [ranking, setRanking] = useState<any[]>([]);
    const [rows, setRows] = useState<Data[]>([]);
    const [order, setOrder] = React.useState<Order>('desc');
    const [orderBy, setOrderBy] = React.useState<keyof Data>('adjustedScore');
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(20);

    const handleRequestSort = (
        event: React.MouseEvent<unknown>,
        property: keyof Data,
    ) => {
        const isAsc = orderBy === property && order === 'desc';
        setOrder(isAsc ? 'asc' : 'desc');
        setOrderBy(property);
    };

    const handleChangePage = (event: unknown, newPage: number) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    const fetchRankings = async (id: string) => {
        const rankingRes = await getLeagueRanking(id);
        setRanking(rankingRes.data);
    }

    // Avoid a layout jump when reaching the last page with empty rows.
    const emptyRows =
        page > 0 ? Math.max(0, (1 + page) * rowsPerPage - rows.length) : 0;

    const visibleRows = React.useMemo(
        () =>
            stableSort(rows, getComparator(order, orderBy)).slice(
                page * rowsPerPage,
                page * rowsPerPage + rowsPerPage,
            ),
        [rows, order, orderBy, page, rowsPerPage],
    );

    useEffect(() => {
        if (leagueId) {
            fetchRankings(leagueId);
        }
    }, [leagueId]);

    useEffect(() => {
        if (ranking.length > 0) {
            setRows(ranking.map((entry, index): any => {
                return {
                    name: entry.player.name,
                    events: Math.round(entry.events),
                    tops: Math.round(entry.tops),
                    adjustedScore: Math.round(entry.adjustedScore),
                    highScore: Math.round(entry.highScore),
                    tier: entry.tier,
                    score: Math.round(entry.score)
                };
            }));
        }
    }, [ranking])

    return (
        <Box sx={{ width: '100%', p: 2 }}>
            <Typography variant="h4">
                {ranking[0]?.league.name}
            </Typography>
            <Box sx={{ width: '100%', p: 1 }}>
                <Paper sx={{ width: '100%', mb: 2 }}>
                    <TableContainer>
                        <Table
                            sx={{ minWidth: 750 }}
                            aria-labelledby="tableTitle"
                        >
                            <RankingTableHead
                                order={order}
                                orderBy={orderBy}
                                onRequestSort={handleRequestSort}
                                rowCount={rows.length}
                            />
                            <TableBody>
                                {visibleRows.map((row, index) => {

                                    return (
                                        <TableRow>
                                            <TableCell align="center">{index + 1 + (page)*rowsPerPage}</TableCell>
                                            <TableCell scope="row">{row.name}</TableCell>
                                            <TableCell align="center">{row.events}</TableCell>
                                            <TableCell align="center">{row.tops}</TableCell>
                                            <TableCell align="center">{row.adjustedScore}</TableCell>
                                            <TableCell align="center">{row.highScore === 0 ? 'N/Q' : row.highScore}</TableCell>
                                            <TableCell align="center">{row.highScore === 0 ? `<${row.tier}>` : row.tier}</TableCell>
                                            <TableCell align="center">{row.score}</TableCell>
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
                        rowsPerPageOptions={[10, 20, 30, 40, 50]}
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