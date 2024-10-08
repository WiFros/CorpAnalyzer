import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axiosInstance from "../axiosInstance";
import { useCompany } from "../context/CompanyContext";
import { Button } from "@nextui-org/react";

const CompanyPage = () => {
  const { selectedCompany } = useCompany();
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // console.log("CompanyPage.js: company:", company);

  useEffect(() => {
    if (!selectedCompany) {
      setIsLoading(false); // selectedCompany가 없으면 로딩을 종료합니다.
    } else {
      setIsLoading(false); // selectedCompany가 있으면 로딩을 종료합니다.
    }
  }, [selectedCompany]);

  if (!selectedCompany) {
    return <div>회사 정보를 찾을 수 없습니다.</div>;
  }

  if (isLoading) {
    return <div>키워드 정보를 불러오는 중입니다...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-3xl font-bold mb-8">
        {selectedCompany.company_name}
      </h1>
      <div className="flex flex-col space-y-4">
        <Button
          onClick={() =>
            navigate(`/company/${selectedCompany.company_id}/info`, {
              state: { company: selectedCompany },
            })
          }
          radius="large"
          className="bg-secondary-300 text-white hover:-translate-y-1 hover:bg-primary-300 transition duration-300 shadow-md py-8 text-lg"
        >
          기업 상세 정보
        </Button>
        <Button
          onClick={() =>
            navigate(`/company/${selectedCompany.company_id}/news`, {
              state: { company: selectedCompany },
            })
          }
          radius="large"
          className="bg-secondary-300 text-white hover:-translate-y-1 hover:bg-primary-300 transition duration-300 shadow-md py-8 text-lg"
        >
          기업 관련 뉴스
        </Button>
        <Button
          onClick={() =>
            navigate(`/company/${selectedCompany.company_id}/keywords`, {
              state: { company: selectedCompany },
            })
          }
          radius="large"
          className="bg-secondary-300 text-white hover:-translate-y-1 hover:bg-primary-300 transition duration-300 shadow-md py-8 text-lg"
        >
          키워드 트렌드
        </Button>
        <Button
          onClick={() =>
            navigate(`/company/${selectedCompany.company_id}/financials`, {
              state: { company: selectedCompany },
            })
          }
          radius="large"
          className="bg-secondary-300 text-white hover:-translate-y-1 hover:bg-primary-300 transition duration-300 shadow-md py-8 text-lg"
        >
          기업 재무제표
        </Button>
      </div>
    </div>
  );
};

export default CompanyPage;
