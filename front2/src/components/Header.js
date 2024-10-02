import { useNavigate } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate();

  const handleLogoClick = () => {
    navigate("/"); // MainSearchPage로 이동
  };

  return (
    <header className="bg-gradient-to-r from-primary-300 to-secondary-300 text-white shadow-lg fixed w-full z-10 transition-shadow duration-300 hover:shadow-2xl">
      <div className="flex items-center justify-between py-4 px-6">
        <h1
          onClick={handleLogoClick}
          className="text-2xl font-bold cursor-pointer font-sans"
        >
          기업 해체 분석기
        </h1>
      </div>
    </header>
  );
};

export default Header;
