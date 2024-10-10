import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import TextSphere from "../components/TextSphere";
import {
  Card,
  Button,
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Link,
} from "@nextui-org/react";
import { Skeleton } from "@nextui-org/skeleton";
import axiosInstance from "../axiosInstance"; // axios 인스턴스를 가져옵니다.

const CompanyKeywordPage = () => {
  const location = useLocation();
  const { company } = location.state || {};
  const [keywords, setKeywords] = useState([]);
  const [isPageLoading, setIsPageLoading] = useState(true); // 페이지 로딩 상태
  const [error, setError] = useState(null);
  const [selectedKeyword, setSelectedKeyword] = useState(null); // 선택한 키워드
  const [newsList, setNewsList] = useState([]); // 키워드에 대한 뉴스 리스트
  const [isModalOpen, setIsModalOpen] = useState(false); // 모달 상태
  const [isModalLoading, setIsModalLoading] = useState(false); // 모달 로딩 상태
  const [backdrop, setBackdrop] = useState("opaque");

  useEffect(() => {
    const fetchHotKeywords = async () => {
      if (!company) return;
      setIsPageLoading(true);
      setError(null);
      try {
        const response = await axiosInstance.get(`/api/companies/hotkeyword`, {
          params: { corp_name: company.company_name },
        });
        setKeywords(response.data.keywords); // 키워드를 상태에 저장
      } catch (error) {
        console.error("키워드 가져오기 오류:", error);
        setError("키워드를 불러오는 데 실패했습니다.");
      } finally {
        setIsPageLoading(false); // 성공 또는 실패 여부에 관계없이 로딩 상태를 false로 설정
      }
    };

    fetchHotKeywords();
  }, [company]);

  // 키워드를 클릭했을 때 해당 키워드의 뉴스를 가져오는 함수
  const handleKeywordClick = async (keyword) => {
    setSelectedKeyword(keyword);
    setIsModalLoading(true); // 모달 로딩 시작
    setIsModalOpen(true);
    try {
      const response = await axiosInstance.get(
        `/api/companies/hotkeyword_with_news`,
        {
          params: { corp_name: company.company_name },
        }
      );
      setNewsList(response.data.keywords[keyword] || []);
    } catch (error) {
      console.error("뉴스 가져오기 오류:", error);
    } finally {
      setIsModalLoading(false); // 모달 로딩 종료
    }
  };

  // 모달을 닫을 때 뉴스 목록을 비우는 함수
  const handleCloseModal = () => {
    setIsModalOpen(false);
    setNewsList([]); // 뉴스 목록 초기화
  };

  const backdrops = ["opaque", "blur", "transparent"];

  if (!company) {
    return <div>회사 정보를 찾을 수 없습니다.</div>;
  }

  return (
    <div className="p-8 flex flex-col items-center justify-center min-h-screen pt-20">
      <h1 className="text-3xl font-bold mb-4">
        {company?.company_name} 키워드 트렌드
      </h1>
      {isPageLoading ? (
        <div className="flex mb-4">
          {/* 스켈레톤 로딩 표시 */}
          <Skeleton className="h-[560px] w-[560px] rounded-md" />
        </div>
      ) : (
        <Card className="flex bg-gradient-to-tr from-primary-300 to-secondary-300 text-white shadow-lg p-4">
          {keywords.length > 0 ? (
            <TextSphere keywords={keywords} onClick={handleKeywordClick} />
          ) : (
            <p>키워드가 없습니다.</p>
          )}
        </Card>
      )}
      {error && <div>{error}</div>} {/* 오류 메시지 표시 */}
      {/* 뉴스 모달 */}
      <Modal
        backdrop={backdrop}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
      >
        <ModalContent>
          <ModalHeader className="flex flex-col gap-1">
            {selectedKeyword} 관련 뉴스
          </ModalHeader>
          <ModalBody>
            {isModalLoading ? ( // 모달 내부에서 로딩 중일 때 메시지 표시
              <p>관련 뉴스를 불러오는 중입니다...</p>
            ) : newsList.length > 0 ? ( // 뉴스가 있을 때 리스트 표시
              <ul>
                {newsList.map((news, index) => (
                  <li
                    key={index}
                    className="mb-4 flex items-center justify-between"
                  >
                    <div>
                      <p className="text-lg font-bold">{news.title}</p>
                      <p>{new Date(news.pubDate).toLocaleString()}</p>
                    </div>
                    <Button
                      as={Link}
                      href={news.link}
                      color="primary"
                      showAnchorIcon
                      variant="light"
                      target="_blank"
                      rel="noopener noreferrer"
                    ></Button>
                  </li>
                ))}
              </ul>
            ) : (
              // 뉴스가 없을 때 메시지 표시
              <p>해당 키워드에 대한 뉴스가 없습니다.</p>
            )}
          </ModalBody>
          <ModalFooter>
            <Button color="primary" variant="light" onClick={handleCloseModal}>
              닫기
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </div>
  );
};

export default CompanyKeywordPage;
