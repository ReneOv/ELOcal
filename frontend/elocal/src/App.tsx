import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { Box } from '@mui/material';
import { ProtectedRoute } from './components/ProtectedRoute';
import { BaseRoutes, AppRoutes } from './routes';
import './App.css';
import { Layout, NoLayout } from './components/Layout';

const Pages = () => {
    return (
        <Box sx={{ display: 'flex', flexGrow: 1 }}>
            <Routes>
                <Route element={<NoLayout />}>
                    {BaseRoutes.map((route, index) => (
                        <Route path={route.path} key={index} element={route.outlet} />
                    ))}
                </Route>
                <Route element={<Layout />}>
                    {AppRoutes.map((route, index) => (
                        <Route
                            path={route.path}
                            key={index}
                            element={<ProtectedRoute outlet={route.outlet} />}
                        />
                    ))}
                </Route>
            </Routes>
        </Box>
    );
};

function App() {
    return (
        <BrowserRouter>
            <Pages />
        </BrowserRouter>
    );
};

export default App;
