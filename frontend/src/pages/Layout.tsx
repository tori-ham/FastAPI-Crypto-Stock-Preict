import { Outlet } from "react-router-dom";
import LeftNavBar from "./LeftNavBar";
import TopBar from "./TopBar";

export default function Layout() {
    return (
        <div className="flex h-screen">
            <LeftNavBar />
            <div className="flex flex-col flex-1">
                <TopBar />
                <div className="flex-1 p-4 overflow-auto">
                    <Outlet />
                </div>
            </div>
        </div>
    )
}