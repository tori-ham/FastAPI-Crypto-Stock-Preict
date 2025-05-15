import { createBrowserRouter } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Forecast from "./pages/Forecast";
import Indicator from "./pages/Indicator";
import News from "./pages/News";
import Settings from "./pages/Settings";
import Layout from "./components/common/Layout";

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