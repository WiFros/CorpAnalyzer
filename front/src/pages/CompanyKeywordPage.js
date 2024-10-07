import { Skeleton } from "@nextui-org/skeleton";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import TextSphere from "../components/TextSphere";
import { Card } from "@nextui-org/react";
import axiosInstance from "../axiosInstance"; // axios 인스턴스를 가져옵니다.

const CompanyKeywordPage = () => {
  const location = useLocation();
  const { company } = location.state || {};
  const [keywords, setKeywords] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHotKeywords = async () => {
      if (!company) return;
      setIsLoading(true);
      setError(null);
      try {
        const response = await axiosInstance.get(`/api/companies/hotkeyword`, {
          params: { corp_name: company.company_name },
        });
        setKeywords(response.data.keywords); // 키워드를 상태에 저장
      } catch (error) {
        console.error("핫 키워드 가져오기 오류:", error);
        setError("키워드를 불러오는 데 실패했습니다.");
      } finally {
        setIsLoading(false); // 성공 또는 실패 여부에 관계없이 로딩 상태를 false로 설정
      }
    };

    fetchHotKeywords();
  }, [company]);

  if (!company) {
    return <div>회사 정보를 찾을 수 없습니다.</div>;
  }

  return (
    <div className="p-8 flex flex-col items-center justify-center min-h-screen pt-20">
      <h1 className="text-3xl font-bold mb-4">
        {company?.company_name} 키워드 트렌드
      </h1>
      {isLoading ? (
        <div className="flex mb-4">
          {/* 스켈레톤 로딩 표시 */}
          <Skeleton className="h-[560px] w-[560px] rounded-md" />
        </div>
      ) : (
        <Card className="flex bg-gradient-to-tr from-green-400 to-blue-500 text-white shadow-lg p-4">
          {keywords.length > 0 ? (
            <TextSphere keywords={keywords} />
          ) : (
            <p>키워드가 없습니다.</p>
          )}
        </Card>
      )}
      {error && <div>{error}</div>} {/* 오류 메시지 표시 */}
    </div>
  );
};

export default CompanyKeywordPage;
