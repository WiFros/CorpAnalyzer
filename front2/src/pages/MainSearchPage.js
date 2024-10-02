import { useState, useEffect, useCallback, useRef } from "react";
import { Input, Spinner } from "@nextui-org/react";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../axiosInstance";
import debounce from 'lodash/debounce';

const MainSearchPage = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const observer = useRef();
  const navigate = useNavigate();

  const lastCompanyElementRef = useCallback(node => {
    if (isLoading) return;
    if (observer.current) observer.current.disconnect();
    observer.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && hasMore) {
        setPage(prevPage => prevPage + 1);
      }
    });
    if (node) observer.current.observe(node);
  }, [isLoading, hasMore]);

  const fetchResults = useCallback(async (query, pageNumber) => {
    if (query.length < 2) {
      setSearchResults([]);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await axiosInstance.get("http://localhost:8000/api/companies/search", {
        params: {
          query: query,
          search_type: "prefix",
          page: pageNumber,
          size: 10  // 한 번에 10개씩 가져오기
        },
      });
      const newResults = response.data.companies;
      setSearchResults(prevResults =>
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
    if (searchTerm) {
      debouncedFetchResults(searchTerm);
    } else {
      setSearchResults([]);
      setPage(1);
    }
  }, [searchTerm, debouncedFetchResults]);

  useEffect(() => {
    if (page > 1) {
      fetchResults(searchTerm, page);
    }
  }, [page, searchTerm, fetchResults]);

  const handleCompanyClick = (companyId) => {
    navigate(`/company/${companyId}`);
  };

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
          <div className="max-h-60 overflow-y-auto border border-gray-300 rounded">
            {searchResults.map((company, index) => (
                <div
                    key={company.company_id}
                    ref={index === searchResults.length - 1 ? lastCompanyElementRef : null}
                    className="p-2 hover:bg-gray-100 cursor-pointer"
                    onClick={() => handleCompanyClick(company.company_id)}
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