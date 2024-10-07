import { RouterProvider } from "react-router-dom";
import { NextUIProvider } from "@nextui-org/react";
import { CompanyProvider } from "./context/CompanyContext.js"
import router from "./router.jsx";


const App = () => {
    return (
        <NextUIProvider>
            <CompanyProvider>
            <div className="flex flex-col min-h-screen">
                <RouterProvider router={router} />
                </div>
            </CompanyProvider>
        </NextUIProvider>
    );
};

export default App;
