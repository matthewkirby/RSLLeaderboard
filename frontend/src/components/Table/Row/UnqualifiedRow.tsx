// components/Table/Row/UnqualifiedRow.tsx
import React from 'react';
import styles from 'css/UnqualifiedRow.module.css';

interface UnqualifiedPlayerData {
  name: string;
  finishes: number;
  tertData?: null;
};

const UnqualifiedRow: React.FC<UnqualifiedPlayerData> = (props) => {
  return (
    <React.Fragment>
      <span className={styles.name}>{props.name}</span>
      <span className={styles.remaining}>
        {3-props.finishes} more finishes to qualify.
      </span>
    </React.Fragment>
  );  
};

export default UnqualifiedRow;
export type { UnqualifiedPlayerData };