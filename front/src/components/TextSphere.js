import React, { useEffect } from "react";
import "../styles/TextShpere.css";
import TagCloud from "TagCloud";

const TextSphere = ({ keywords }) => {
  // Animation settings for Text Cloud
  useEffect(() => {
    // 텍스트 구름 초기화
    const container = ".tagcloud";

    const options = {
      radius: 300,
      maxSpeed: "fast",
      initSpeed: "normal",
      keep: true,
    };

    TagCloud(container, keywords, options); // keywords로 텍스트 구름 설정

    return () => {
      // cleanup function
    };
  }, [keywords]); // keywords가 변경될 때마다 호출

  return (
    <div className="text-shpere">
      <span className="tagcloud"></span>
    </div>
  );
};

export default TextSphere;
