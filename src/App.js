import React from "react";
import { RouterProvider } from "react-router-dom";
import { NextUIProvider } from "@nextui-org/react";
import router from "./router";

const App = () => {
  return (
    <NextUIProvider>
      <div className="flex flex-col min-h-screen">
        <RouterProvider router={router} />
      </div>
    </NextUIProvider>
  );
};

export default App;
