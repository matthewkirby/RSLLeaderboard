// components/NavBar/NavBar.tsx
import React from "react";
import { Link, Outlet } from "react-router-dom";

const NavBar: React.FC = () => {
  return (
    <React.Fragment>
      <Link to="/">Leaderboard</Link>
      <Link to="/races">Race History</Link>
      <Outlet />
    </React.Fragment>
  );
}

export default NavBar;