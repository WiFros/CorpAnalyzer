import { useLocation, Link } from "react-router-dom";
import axiosInstance from "../axiosInstance";

const CompanyPage = () => {
  const location = useLocation();
  const { company } = location.state || {};
  console.log("CompanyPage.js: company:", company);
  // api 요청

  try {
    const response = axiosInstance.get(`/api/companies/hotkeyword`, {
      params: { corp_name: company.company_name }
    });
    console.log("Hot Keywords:", response.data.keywords);
  } catch (error) {
    console.error("핫 키워드 가져오기 오류:", error);
    if (error.response) {
      console.error("Error response:", error.response.data);
      console.error("Error status:", error.response.status);
      console.error("Error headers:", error.response.headers);
    } else if (error.request) {
      console.error("Error request:", error.request);
    } else {
      console.error("Error message:", error.message);
    }
  }

  if (!company) {
    return <div>회사 정보를 찾을 수 없습니다.</div>;
  }

  return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <h1 className="text-3xl font-bold mb-8">{company.company_name}</h1>
        <div className="flex flex-col space-y-4">
          <Link to={`/company/${company.company_id}/info`} state={{ company }} className="btn">
            기업 상세 정보
          </Link>
          <Link to={`/company/${company.company_id}/news`} state={{ company }} className="btn">
            기업 관련 뉴스
          </Link>
          <Link to={`/company/${company.company_id}/keywords`} state={{ company }} className="btn">
            키워드 트렌드
          </Link>
          <Link to={`/company/${company.company_id}/financials`} state={{ company }} className="btn">
            기업 재무제표
          </Link>
        </div>
      </div>
  );
};

export default CompanyPage;