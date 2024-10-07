import { useEffect, useState, useCallback } from "react";
import { useLocation } from "react-router-dom";
import axiosInstance from "../axiosInstance";
import { Card, CardHeader, CardBody, Divider } from "@nextui-org/react";

const CompanyInfoPage = () => {
  const location = useLocation();
  const company = location.state?.company; // 상태로 넘어온 회사 정보
  const [info, setInfo] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // API 호출 함수를 useCallback으로 감싸서 의존성 관리
  const fetchCompanyInfo = useCallback(async () => {
    if (!company) return;

    setIsLoading(true);
    setError(null);
    try {
      // 회사 이름을 URL 패스에 포함시킴
      const response = await axiosInstance.get(
        `/dart_analyze/dart_reports/${encodeURIComponent(company.company_name)}`
      );
      setInfo(response.data.data); // JSON 데이터 구조에 맞춰 수정
    } catch (err) {
      console.error("정보를 가져오는 중 오류가 발생했습니다:", err);
      setError("정보를 불러오는 중 오류가 발생했습니다.");
    } finally {
      setIsLoading(false);
    }
  }, [company]);

  useEffect(() => {
    fetchCompanyInfo(); // 컴포넌트 마운트 시 API 호출
  }, [fetchCompanyInfo]); // fetchCompanyInfo가 변경될 때만 호출

  if (isLoading) {
    return <div>로딩 중...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="p-8" style={{ paddingTop: "80px" }}>
      <h1 className="text-3xl font-bold mb-4">{info.company_name}</h1>

      <Card className="mb-6" style={{ maxWidth: "600px", margin: "0 auto" }}>
        <CardHeader className="font-bold">주요 사업 내용</CardHeader>
        <Divider />
        <CardBody>{info.result.business_overview}</CardBody>
      </Card>

      <Card className="mb-6" style={{ maxWidth: "600px", margin: "0 auto" }}>
        <CardHeader className="font-bold">주요 제품 및 서비스</CardHeader>
        <Divider />
        <CardBody>{info.result.products_and_sales}</CardBody>
      </Card>

      <Card className="mb-6" style={{ maxWidth: "600px", margin: "0 auto" }}>
        <CardHeader className="font-bold">
          주요 계약 및 연구 개발 활동
        </CardHeader>
        <Divider />
        <CardBody>{info.result.contracts_and_rnd}</CardBody>
      </Card>
    </div>
  );
};

export default CompanyInfoPage;
