import { Outlet } from 'react-router-dom';
import { Sidebar } from '../Sidebar';
import { Box, Typography } from '@mui/material';

interface Props {
    children?: any;
}

export const NoLayout = ({ children }: Props) => {
    return (
        <div style={{ width: '100%' }}>
            <div className="p-4 container__children">
                <Outlet />
                {children}
            </div>
        </div>
    );
};

export const Layout = ({ children }: Props) => {
    return (
        <div>
            <Sidebar />
            <Box component="main" sx={{ flexGrow: 1, p: 10}}>
                <Outlet />
                {children}
            </Box>
        </div>
    );
}