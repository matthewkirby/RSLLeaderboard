// components/NavBar/NavButton.tsx
import React from "react";
import { Link } from "react-router-dom";
import styles from "css/NavButton.module.css"

type Variant = "primary";

interface NavButtonProps {
  destination: string,
  variant?: Variant,
  children: React.ReactNode
}

const NavButton: React.FC<NavButtonProps> = (props) => {
  const variant: Variant = props.variant || "primary";

  return (
    <Link to={props.destination}>
      <div className={styles[variant]}>
        {props.children}
      </div>
    </Link>
  );
};

export default NavButton;