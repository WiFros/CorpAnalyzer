
import { useLocation, Link } from "react-router-dom";

const CompanyPage = () => {
  const location = useLocation();
  const { company_name, company_id } = location.state || {}; // 검색 결과에서 기업 이름을 받아옴

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-3xl font-bold mb-8">{company_name}</h1>{" "}
      {/* 기업 이름 표시 */}
      <div className="flex flex-col space-y-4">
        <Link to="/companyInfo" state={{ company_id }} className="btn">
          기업 상세 정보
        </Link>
        <Link to="/companyNews" state={{ company_id }} className="btn">
          기업 관련 뉴스
        </Link>
        <Link to="/companyKeyword" state={{ company_id }} className="btn">
          키워드 트렌드
        </Link>
        <Link to="/companyFinance" state={{ company_id }} className="btn">
          기업 재무제표
        </Link>
      </div>
    </div>
  );
};

export default CompanyPage;
