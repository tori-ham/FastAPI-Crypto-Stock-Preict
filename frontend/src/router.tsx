import { createBrowserRouter } from "react-router-dom";
import Dashboard from "./pages/dashboard/Dashboard";
import Forecast from "./pages/forecast/Forecast";
import Indicator from "./pages/indicator/Indicator";
import News from "./pages/news/News";
import Settings from "./pages/settings/Settings";
import Layout from "./pages/Layout";

const router= createBrowserRouter(
    [
        {
            path: '/',
            element: <Layout />,
            children: [
                {
                    index: true,
                    element: <Dashboard />
                }, {
                    path: '/forecast',
                    element: <Forecast />
                }, {
                    path: '/indicator',
                    element: <Indicator />
                }, {
                    path: '/news',
                    element: <News />
                }, {
                    path: '/settings',
                    element: <Settings />
                }
            ]
        }
    ]
);

export default router;