import { useEffect, useState, useCallback } from "react";
import { useLocation } from "react-router-dom";
import axiosInstance from "../axiosInstance";
import {
  Card,
  CardHeader,
  CardBody,
  Divider,
  Textarea,
  Link,
  Button,
} from "@nextui-org/react";

const CompanyNewsPage = () => {
  const location = useLocation();
  const company = location.state?.company; // 상태로 넘어온 회사 정보
  const [news, setNews] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // API 호출 함수
  const fetchCompanyNews = useCallback(async () => {
    if (!company) return;

    setIsLoading(true);
    setError(null);
    try {
      // 회사 이름을 URL 패스에 포함시킴
      const response = await axiosInstance.get(
        `/api/companies/news/${encodeURIComponent(company.company_name)}`
      );
      setNews(response.data);
    } catch (err) {
      console.error("뉴스를 가져오는 중 오류가 발생했습니다:", err);
      setError("뉴스를 불러오는 중 오류가 발생했습니다.");
    } finally {
      setIsLoading(false);
    }
  }, [company]);

  useEffect(() => {
    fetchCompanyNews();
  }, [fetchCompanyNews]);

  if (isLoading) {
    return <div>로딩 중...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  const { result, company_name, news: newsList } = news; // 데이터 구조 해체

  return (
    <div className="p-8" style={{ paddingTop: "100px", textAlign: "center" }}>
      <h1 className="text-3xl font-bold mb-4 font-kopub">{result?.title}</h1>
      {result?.move.map((moveItem, index) => (
        <Card
          key={index}
          className="mb-6 font-gothic"
          style={{
            maxWidth: "600px",
            margin: "0 auto",
            padding: "0.5rem",
            marginBottom: "20px",
          }}
        >
          <CardHeader
            className="font-bold"
            style={{ position: "relative", zIndex: 0 }}
          >
            {moveItem.field}
          </CardHeader>
          <Divider />
          <CardBody>
            <ul>
              {moveItem.current_activity.map((activity, idx) => (
                <li key={idx} className="mb-1">
                  {activity}
                </li>
              ))}
            </ul>
          </CardBody>
        </Card>
      ))}
      <div
        className="mx-auto flex flex-col items-center mt-6 max-w-[700px]"
        style={{ textAlign: "center" }}
      >
        <h3 className="text-xl font-bold mb-4">요약</h3>
        <Textarea
          isReadOnly
          variant="bordered"
          defaultValue={result?.summary}
          className="mb-6 font-gothic"
          style={{
            height: "auto", // 텍스트 크기에 맞게 높이 자동 조정
            fontSize: "18px", // 폰트 크기 설정 (글자 더 크게)
            lineHeight: "1.8", // 줄 간격 조정
            padding: "0.7rem", // 내부 패딩 추가
          }}
        />
      </div>
      <div
        className="max-w-[800px]"
        style={{
          margin: "0 auto",
          textAlign: "center",
          marginTop: "40px",
          marginBottom: "80px",
        }}
      >
        <h1 className="text-2xl font-bold mb-6">{company_name} 최신 뉴스</h1>
        <Card style={{ maxWidth: "700px", margin: "0 auto", padding: "1rem" }}>
          {newsList && newsList.length > 0 ? (
            <ul>
              {newsList.map((newsItem, idx) => (
                <li
                  key={idx}
                  className="flex justify-between items-center mb-3"
                >
                  <span className="text-lg font-medium font-gothic">
                    {newsItem.title}
                  </span>
                  {/* 링크가 "no data"가 아닐 때만 버튼을 렌더링 */}
                  {newsItem.link && newsItem.link !== "no data" ? (
                    <Button
                      as={Link}
                      href={newsItem.link}
                      color="primary"
                      showAnchorIcon
                      variant="light"
                      target="_blank"
                      rel="noopener noreferrer"
                    ></Button>
                  ) : null}
                </li>
              ))}
            </ul>
          ) : (
            <div
              className="flex justify-center items-center"
              style={{ height: "100px" }}
            >
              <p className="text-lg font-gothic text-center">
                최신 뉴스가 없습니다.
              </p>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default CompanyNewsPage;
