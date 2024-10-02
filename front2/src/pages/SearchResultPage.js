import { useState } from "react";
import { useLocation, Link } from "react-router-dom";

const SearchResultPage = () => {
  const location = useLocation();
  const { results } = location.state || {}; // 전달된 검색 결과를 가져옴

  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = results.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(results.length / itemsPerPage);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">검색 결과</h1>
      {currentItems.length > 0 ? (
        <ul className="mb-4">
          {currentItems.map((item) => (
            <li key={item.company_id} className="border-b py-2">
              <Link
                to="/company"
                state={{
                  company_name: item.company_name,
                  company_id: item.company_id,
                }} // 이름과 ID 전달
                className="text-blue-500 hover:underline"
              >
                {item.name}
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p>검색 결과가 없습니다.</p>
      )}

      {/* 페이지네이션 */}
      <div className="flex justify-center mt-4">
        {Array.from({ length: totalPages }, (_, index) => (
          <button
            key={index + 1}
            onClick={() => handlePageChange(index + 1)}
            className={`px-4 py-2 mx-1 ${
              currentPage === index + 1
                ? "bg-blue-500 text-white"
                : "bg-gray-200"
            } rounded`}
          >
            {index + 1}
          </button>
        ))}
      </div>
    </div>
  );
};

export default SearchResultPage;
