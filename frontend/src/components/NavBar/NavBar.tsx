// components/NavBar/NavBar.tsx
import React from "react";
import { Outlet } from "react-router-dom";
import NavButton from "./NavButton";
import styles from "css/NavBar.module.css"

const NavBar: React.FC = () => {
  return (
    <React.Fragment>
      <span className={styles.container}>
        <NavButton destination="/">
          Leaderboard
        </NavButton>
        <NavButton destination="/races">
          Race History
        </NavButton>
      </span>
      <Outlet />
    </React.Fragment>
  );
}

export default NavBar;