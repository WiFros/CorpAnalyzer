import { useEffect, useRef } from "react";
import "../styles/TextShpere.css";
import TagCloud from "TagCloud";

const TextSphere = ({ keywords }) => {
  const containerRef = useRef(null);
  useEffect(() => {
    if (containerRef.current && keywords.length > 0) {
      const container = containerRef.current;
      container.innerHTML = '';

      const options = {
        radius: 300,
        maxSpeed: "fast",
        initSpeed: "normal",
        keep: true,
      };

      TagCloud(container, keywords, options);
    }

    return () => {
      if (containerRef.current) {
        containerRef.current.innerHTML = '';
      }
    };
  }, [keywords]);

  return (
      <div className="text-sphere">
        <span ref={containerRef} className="tagcloud"></span>
      </div>
  );
};

export default TextSphere;