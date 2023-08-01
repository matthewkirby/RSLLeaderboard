// components/Loading.tsx
import React from 'react';
import styles from "css/Loading.module.css";

const Loading: React.FC = () => {
  return (
    <div className={styles.container}>
      <span className={styles.text}>Loading...</span>
      <svg className={styles.graphic} version="1.1" viewBox="0 0 157.47 136.59" xmlns="http://www.w3.org/2000/svg">
        <g fill="#d7d000" fillRule="evenodd">
          <path transform="matrix(1.4137 0 0 1.4131 -34.298 61.671)" d="m79.893 53.017-55.632-1e-6 27.816-48.179z" stopColor="#000000"/>
          <path transform="matrix(1.4137 0 0 1.4131 5.213 -6.8373)" d="m79.893 53.017-55.632-1e-6 27.816-48.179z" stopColor="#000000"/>
          <path transform="matrix(1.4137 0 0 1.4131 44.519 61.242)" d="m79.893 53.017-55.632-1e-6 27.816-48.179z" stopColor="#000000"/>
        </g>
      </svg>
    </div>
  );
};

export default Loading;