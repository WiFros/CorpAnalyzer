import { createBrowserRouter } from "react-router-dom";
import Layout from "./components/Layout";
import MainSearchPage from "./pages/MainSearchPage";
import CompanyPage from "./pages/CompanyPage";
import CompanyInfoPage from "./pages/CompanyInfoPage";
import CompanyNewsPage from "./pages/CompanyNewsPage";
import CompanyKeywordPage from "./pages/CompanyKeywordPage";
import CompanyFinancialPage from "./pages/CompanyFinancialPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        path: "",
        element: <MainSearchPage />,
      },
      {
        path: "company/:company_id",
        element: <CompanyPage />,
      },
      {
        path: "company/:company_id/info",
        element: <CompanyInfoPage />,
      },
      {
        path: "company/:company_id/news",
        element: <CompanyNewsPage />,
      },
      {
        path: "company/:company_id/keywords",
        element: <CompanyKeywordPage />,
      },
      {
        path: "company/:company_id/financials",
        element: <CompanyFinancialPage />,
      },
    ],
  },
]);

export default router;