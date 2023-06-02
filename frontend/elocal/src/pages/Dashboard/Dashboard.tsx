import { Box, Typography } from "@mui/material";

export const Dashboard = () => {
    return (
        <Box sx={{ width: '100%', p: 2 }}>
            <Typography variant="h2">
                Bienvenid@ a ELOcal!
            </Typography>
            <Box sx={{ width: '100%', p: 2 }}>
                <Typography variant="h5">
                    Aquí podrás consultar el detalle de todos los eventos registrados que se usaron para los ratings y rankings.
                    <br/>
                    También podrás ver los ratings al momento de cada liga!
                </Typography>
            </Box>
        </Box>
    );
}