// components/Table/Table.tsx
import React from 'react';
import styles from './Table.module.css';
import rowComponents, { DataVariants, TableVariants } from './Row';

interface TableProps {
  primaryHeading: string[];
  secondaryHeading?: string;
  variant: TableVariants;
  data: DataVariants[];
}

const Table: React.FC<TableProps> = ({ primaryHeading, secondaryHeading, variant, data }) => {
  const SubComponent = rowComponents[variant];
  if (!SubComponent) {
    console.log(`--${variant} is not a valid Table RowComponent`);
    return null;
  }

  return (
    <ol className={styles.table}>
      <li className={styles.header}>
        {primaryHeading.map((text, index) => <h4 key={index} className={styles.primaryHeader}>{text}</h4>)}
      </li>
      {data.map((player) => (
        <li className={styles.row} key={player.name}>
          <SubComponent key={player.name} {...player} />
        </li>
      ))}
    </ol>
  );
};

export default Table;