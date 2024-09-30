import React, { useState } from "react";
import { Button, Input } from "@nextui-org/react";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../axiosInstance";

const MainSearchPage = () => {
  const [searchTerm, setSearchTerm] = useState(""); // 검색어 상태
  const navigate = useNavigate();

  const handleSearch = async (e) => {
    e.preventDefault();

    try {
      // GET 요청으로 검색어를 보내고 데이터를 받아옴
      const response = await axiosInstance.get("/companies/search", {
        params: { query: searchTerm },
      });

      const results = response.data; // 응답 데이터 (company_id, name)

      // 검색 결과 페이지로 이동하며 데이터를 전달
      navigate("/search-results", { state: { results } });
    } catch (error) {
      console.error("검색 중 오류 발생:", error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-4xl font-sans font-bold mb-8">기업 검색</h1>
      <form onSubmit={handleSearch} className="flex w-full max-w-md font-sans">
        <Input
          size={"lg"}
          isClearable
          bordered
          fullWidth
          placeholder="기업 이름을 입력하세요"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onClear={() => setSearchTerm("")}
          className=""
        />
        <Button
          radius="full"
          type="submit"
          size="lg"
          className="bg-gradient-to-tr from-pink-500 to-yellow-500 text-white shadow-md mx-2"
        >
          검색
        </Button>
      </form>
    </div>
  );
};

export default MainSearchPage;
