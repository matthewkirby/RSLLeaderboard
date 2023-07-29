// components/NavBar/Logo.tsx
import React from "react";
import styles from "css/Logo.module.css"

const Logo: React.FC = () => {
  return (
    <div className={styles.logoArea}>
      {/* <svg className={styles.logo} width="35px" height="35px"></svg> */}
      <div className={styles.logoText}>RSL</div>
    </div>
  );
}

export default Logo;