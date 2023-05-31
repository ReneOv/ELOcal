import { EmojiEvents, Event, Home } from "@mui/icons-material";

import { Dashboard } from "../pages/Dashboard";

interface SubChildren {
    path: string;
    name: string;
    icon: JSX.Element | '';
    sidebar: boolean;
}

interface Children {
    path: string;
    icon: JSX.Element | '';
    sidebar: boolean;
    name: string;
    subChildren?: SubChildren[];
}

interface Route {
    path: string;
    name: string;
    icon: JSX.Element | '';
    sidebar: boolean;
    outlet: JSX.Element;
    children?: Children[];
}

export const BaseRoutes: Route[] = [
    // Login
    {
        name: 'Login',
        path: '/login',
        icon: '',
        outlet: <>Login</>,
        sidebar: false
    },
    // Error 404
    {
        name: 'Error 404',
        path: '*',
        icon: '',
        outlet: <>404</>,
        sidebar: false
    }
];

export const AppRoutes: Route[] = [
    // Home
    {
        name: 'Home',
        path: '/',
        icon: <Home />,
        outlet: <Dashboard />,
        sidebar: true
    },
    // Leagues
    {
        name: 'Leagues',
        path: '/leagues',
        icon: <EmojiEvents />,
        outlet: <>Leagues</>,
        sidebar: true
    },
    // Events
    {
        name: 'Events',
        path: '/events',
        icon: <Event />,
        outlet: <>Events</>,
        sidebar: true
    }
]