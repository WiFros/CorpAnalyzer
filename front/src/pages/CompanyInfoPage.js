import { useEffect, useState, useCallback } from "react";
import { useLocation } from "react-router-dom";

const CompanyInfoPage = () => {
  const location = useLocation();
  const { company_id } = location.state || {};
  const [companyInfo, setCompanyInfo] = useState(null);

  // API 호출 함수를 useCallback으로 감싸서 의존성 관리
  const fetchCompanyInfo = useCallback(async () => {
    try {
      const response = await fetch(`/companies/${company_id}`);
      if (!response.ok) throw new Error("Network response was not ok");
      const data = await response.json();
      setCompanyInfo(data);
    } catch (error) {
      console.error("Fetch error:", error);
    }
  }, [company_id]); // company_id가 변경될 때만 함수가 새로 생성됨

  useEffect(() => {
    fetchCompanyInfo(); // 컴포넌트 마운트 시 API 호출
  }, [fetchCompanyInfo]); // fetchCompanyInfo가 변경될 때만 호출

  return (
    <div className="p-8">
      {companyInfo ? (
        <div>
          <h1 className="text-3xl font-bold mb-4">{companyInfo.name}</h1>
          <p>
            <strong>산업:</strong> {companyInfo.industry}
          </p>
          <p>
            <strong>설명:</strong> {companyInfo.description}
          </p>
          <p>
            <strong>설립일:</strong> {companyInfo.foundation_date}
          </p>
          <p>
            <strong>웹사이트:</strong>{" "}
            <a
              href={companyInfo.website}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500"
            >
              {companyInfo.website}
            </a>
          </p>
          <p>
            <strong>직원 수:</strong> {companyInfo.employees}
          </p>
          <p>
            <strong>수익:</strong> {companyInfo.revenue.toLocaleString()} 원
          </p>
        </div>
      ) : (
        <p>기업 정보를 불러오는 중입니다...</p>
      )}
    </div>
  );
};

export default CompanyInfoPage;
