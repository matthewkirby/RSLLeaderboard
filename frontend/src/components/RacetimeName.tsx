// components/RacetimeName.tsx
import React from 'react';
import styles from "css/RacetimeName.module.css";

interface RacetimeNameProps {
  name: string,
  discriminator: string | null
}

const RacetimeName: React.FC<RacetimeNameProps> = ({ name, discriminator }) => {
  return (
    <span className={styles.name}>
      {name}
      {discriminator !== null ? <span className={styles.discriminator}>{`#${discriminator}`}</span> : null}
    </span>
  );
};

export default RacetimeName;