// components/NavBar/NavButton.tsx
import React from "react";
import { NavLink } from "react-router-dom";
import styles from "css/NavButton.module.css"

interface NavButtonProps {
  destination: string,
  content: React.ReactNode
}

const NavButton: React.FC<NavButtonProps> = (props) => {

  return (
    <li>
      <NavLink
        to={props.destination}
        className={({isActive}) =>
          isActive ? `${styles.link} ${styles.active}` : styles.link
        }
      >
        {props.content}
      </NavLink>
    </li>
  );
};

export default NavButton;