import { useEffect, useState } from "react";
import { useParams, useLocation } from "react-router-dom";
import TextSphere from "../components/TextSphere";
import axiosInstance from "../axiosInstance";

const CompanyKeywordPage = () => {
  const { company_id } = useParams();
  const location = useLocation();
  const { company } = location.state || {};
  const [keywords, setKeywords] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  console.log("CompanyKeywordPage.js: company:", company);

  useEffect(() => {
    const fetchHotKeywords = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await axiosInstance.get(`/api/companies/hotkeyword`, {
          params: { corp_name: company.company_name }
        });
        console.log("Hot Keywords:", response.data.keywords);
        setKeywords(response.data.keywords); // 여기서 상태 업데이트가 필요합니다.
        setIsLoading(false); // 데이터를 성공적으로 가져온 후 로딩 상태를 해제합니다.
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
        setError("키워드를 불러오는 데 실패했습니다.");
        setIsLoading(false); // 오류 발생 시에도 로딩 상태를 해제합니다.
      }

    };

    if (company && company.company_name) {
      fetchHotKeywords();
    } else {
      setError("회사 정보를 찾을 수 없습니다.");
      setIsLoading(false);
    }
  }, [company]);

  if (isLoading) {
    return <div>키워드 정보를 불러오는 중입니다...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
      <div className="p-8">
        <h1 className="text-3xl font-bold mb-4">{company?.company_name} 키워드 트렌드</h1>
        {keywords.length > 0 ? (
            <TextSphere keywords={keywords} />
        ) : (
            <p>키워드가 없습니다.</p>
        )}
      </div>
  );
};

export default CompanyKeywordPage;