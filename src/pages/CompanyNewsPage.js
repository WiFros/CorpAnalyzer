import React, { useEffect, useState, useCallback } from "react";
import { useLocation } from "react-router-dom";

const CompanyNewsPage = () => {
  const location = useLocation();
  const { company_id } = location.state || {}; // 회사 ID를 받아옴
  const [newsList, setNewsList] = useState([]); // 뉴스 목록 상태

  // API 호출 함수
  const fetchCompanyNews = useCallback(async () => {
    try {
      const response = await fetch(`/companies/${company_id}/news`);
      if (!response.ok) throw new Error("Network response was not ok");
      const data = await response.json();
      setNewsList(data); // 받아온 뉴스 데이터를 상태에 저장
    } catch (error) {
      console.error("Fetch error:", error);
    }
  }, [company_id]); // company_id가 변경될 때마다 호출

  useEffect(() => {
    fetchCompanyNews(); // 컴포넌트 마운트 시 API 호출
  }, [fetchCompanyNews]); // fetchCompanyNews가 변경될 때만 호출

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">뉴스 목록</h1>
      {newsList.length > 0 ? (
        <ul>
          {newsList.map((news) => (
            <li key={news.news_id} className="border-b py-4">
              <h2 className="text-xl font-semibold">{news.title}</h2>
              <p>{news.summary}</p>
              <p className="text-gray-500">
                {new Date(news.publish_date).toLocaleDateString()}
              </p>
              <a
                href={news.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500"
              >
                자세히 보기
              </a>
            </li>
          ))}
        </ul>
      ) : (
        <p>뉴스 정보를 불러오는 중입니다...</p>
      )}
    </div>
  );
};

export default CompanyNewsPage;
