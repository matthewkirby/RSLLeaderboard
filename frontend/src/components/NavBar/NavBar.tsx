// components/NavBar/NavBar.tsx
import React from "react";
import { Outlet } from "react-router-dom";
import NavButton from "./NavButton";
import styles from "css/NavBar.module.css"
import Logo from "./Logo";

const NavBar: React.FC = () => {
  return (
    <React.Fragment>
      <header className={styles.header} id="site-header">
        <Logo />
        <div className={styles.navigationArea}>
          <ul className={styles.mainNav}>
            <NavButton destination="/" content="Leaderboard" />
            <NavButton destination="/races" content="Race History" />
          </ul>
        </div>
      </header>
      <Outlet />
    </React.Fragment>
  );
}

export default NavBar;