import { useEffect, useRef } from "react";
import "../styles/TextShpere.css";
import TagCloud from "TagCloud";

const TextSphere = ({ keywords, onClick }) => {
  const containerRef = useRef(null);
  useEffect(() => {
    if (containerRef.current && keywords.length > 0) {
      const container = containerRef.current;
      container.innerHTML = "";

      const options = {
        radius: 270,
        maxSpeed: "fast",
        initSpeed: "normal",
        keep: true,
      };

      TagCloud(container, keywords, options);

      // 각 키워드에 클릭 이벤트 추가
      const tagItems = container.getElementsByTagName("span");
      Array.from(tagItems).forEach((item, index) => {
        item.addEventListener("click", () => {
          onClick(keywords[index]);
        });
      });
    }

    return () => {
      if (containerRef.current) {
        containerRef.current.innerHTML = "";
      }
    };
  }, [keywords, onClick]);

  return (
    <div className="text-shpere">
      <span ref={containerRef} className="tagcloud"></span>
    </div>
  );
};

export default TextSphere;
