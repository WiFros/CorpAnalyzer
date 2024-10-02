import React, { useEffect, useState, useCallback } from "react";
import { useLocation } from "react-router-dom";
import TextSphere from "../components/TextSphere";

const CompanyKeywordPage = () => {
  const location = useLocation();
  const { company_id } = location.state || {}; // 회사 ID를 받아옴
  const [keywords, setKeywords] = useState([]); // 키워드 상태

  // API 호출 함수
  const fetchKeywordTrends = useCallback(async () => {
    try {
      const response = await fetch(`/companies/${company_id}/keyword-trends`);
      if (!response.ok) throw new Error("Network response was not ok");
      const data = await response.json();
      const keywordsArray = data.trends.map((trend) => trend.keyword); // 키워드만 추출
      setKeywords(keywordsArray); // 키워드를 상태에 저장
    } catch (error) {
      console.error("Fetch error:", error);
    }
  }, [company_id]); // company_id가 변경될 때마다 호출

  useEffect(() => {
    fetchKeywordTrends(); // 컴포넌트 마운트 시 API 호출
  }, [fetchKeywordTrends]); // fetchKeywordTrends가 변경될 때만 호출

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">키워드 트렌드</h1>
      {keywords.length > 0 ? (
        <TextSphere keywords={keywords} /> // 키워드를 TextSphere에 전달
      ) : (
        <p>키워드 정보를 불러오는 중입니다...</p>
      )}
    </div>
  );
};

export default CompanyKeywordPage;
