import { useState, useEffect, useCallback, useRef } from "react";
import { Input, Spinner } from "@nextui-org/react";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../axiosInstance";
import debounce from "lodash/debounce";
import { useCompany } from "../context/CompanyContext.js";

const MainSearchPage = () => {
  const { setSelectedCompany } = useCompany();
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const observer = useRef();
  const navigate = useNavigate();

  const handleCompanyClick = async function (company) {
    console.log("Navigating to company page for:", company.company_name);
    setSelectedCompany(company);
    if (company && company.company_id) {
      navigate(`/company/${company.company_id}`, { state: { company } });
    } else {
      console.error("Company object is invalid or missing required properties");
    }
  };
  const lastCompanyElementRef = useCallback(
    (node) => {
      if (isLoading) return;
      if (observer.current) observer.current.disconnect();
      observer.current = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && hasMore) {
          setPage((prevPage) => prevPage + 1);
        }
      });
      if (node) observer.current.observe(node);
    },
    [isLoading, hasMore]
  );

  const fetchResults = useCallback(async (query, pageNumber) => {
    if (query.length < 2) {
      setSearchResults([]);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await axiosInstance.get("/api/companies/search", {
        params: {
          query: query,
          search_type: "prefix",
          page: pageNumber,
          size: 10, // 한 번에 10개씩 가져오기
        },
      });
      const newResults = response.data.companies;
      setSearchResults((prevResults) =>
        pageNumber === 1 ? newResults : [...prevResults, ...newResults]
      );
      setHasMore(newResults.length > 0);
    } catch (error) {
      console.error("검색 중 오류 발생:", error);
      setError("검색 중 오류가 발생했습니다. 다시 시도해 주세요.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  const debouncedFetchResults = useCallback(
    debounce((query) => {
      setPage(1);
      fetchResults(query, 1);
    }, 300),
    []
  );

  useEffect(() => {
    // 검색어가 있을 때
    if (searchTerm) {
      debouncedFetchResults(searchTerm);
      setSelectedCompany(null);
    } else {
      // 검색어가 비어 있을 때 이전 검색 결과 및 상태 초기화
      setSearchResults([]);
      setPage(1);
    }
  }, [searchTerm, debouncedFetchResults, setSelectedCompany]);

  useEffect(() => {
    if (page > 1) {
      fetchResults(searchTerm, page);
    }
  }, [page, searchTerm, fetchResults]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 className="text-4xl font-sans font-bold mb-8">기업 검색</h1>
      <div className="w-full max-w-md">
        <Input
          size="lg"
          isClearable
          bordered
          fullWidth
          placeholder="기업 이름을 입력하세요"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onClear={() => setSearchTerm("")}
          className="mb-4"
        />
        {error && <p className="text-red-500 mb-2">{error}</p>}
        <div className="max-h-60 overflow-y-auto border-gray-300 rounded">
          {searchResults.map((company, index) => (
            <div
              key={company.company_id}
              ref={
                index === searchResults.length - 1
                  ? lastCompanyElementRef
                  : null
              }
              className="p-2 hover:bg-gray-100 cursor-pointer"
              onClick={() => handleCompanyClick(company)}
            >
              {company.company_name}
            </div>
          ))}
          {isLoading && <Spinner className="m-2" />}
        </div>
      </div>
    </div>
  );
};

export default MainSearchPage;
