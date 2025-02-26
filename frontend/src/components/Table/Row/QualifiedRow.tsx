// components/Table/Row/QualifiedRow.tsx
import React from 'react';
import { getOrdinal, addPlacementClass } from "utils/formatting";
import styles from 'css/QualifiedRow.module.css';

interface QualifiedPlayerData {
  name: string;
  entries: number;
  finishes: number;
  rating: number;
  placement: number;
  tertData?: null;
};

const QualifiedRow: React.FC<QualifiedPlayerData> = (props) => {
  const ordinal = getOrdinal(props.placement);

  return (
    <React.Fragment>
      <span className={`${styles.placement} ${addPlacementClass(ordinal)}`}>{ordinal}</span>
      <span className={styles.name}>{props.name}</span>
      <span className={styles.rating}>{props.rating}</span>
      <span className={styles.extraData}>
        <span className={styles.finishes}>{props.finishes} Finishes</span>
        <span className={styles.entries}>{props.entries} Races</span>
      </span>
    </React.Fragment>
  );  
};

export default QualifiedRow;
export type { QualifiedPlayerData };