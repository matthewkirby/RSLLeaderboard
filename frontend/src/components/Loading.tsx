// components/Loading.tsx
import React from 'react';
import styles from "css/Loading.module.css";

const Loading: React.FC = () => {
  return (
    <div className={styles.container}>
      <span className={styles.text}>Loading...</span>
      <img src="/images/Loading.svg" className={styles.graphic} alt="Loading..." />
    </div>
  );
};

export default Loading;