// components/Table/Table.tsx
import React, { useState } from 'react';
import styles from 'css/Table.module.css';
import rowComponents, { DataVariants, TableVariants } from './Row';
import Loading from 'components/Loading';

type handlerFunctionType = () => React.ReactNode;

interface TableProps {
  primaryHeading: string[];
  secondaryHeading?: string;
  variant: TableVariants;
  data: DataVariants[] | undefined;
  parentDataLoading?: boolean;
  callable?: React.MouseEventHandler<HTMLButtonElement>;
}

const Table: React.FC<TableProps> = ({ primaryHeading, secondaryHeading, variant, data, parentDataLoading, callable }) => {
  const [loading, setLoading] = useState<boolean>(parentDataLoading ?? false);

  const SubComponent = rowComponents[variant];
  if (!SubComponent) {
    console.log(`--${variant} is not a valid Table RowComponent`);
    return null;
  }

  function onClick(e: React.MouseEvent<HTMLButtonElement>): void {
    if(callable !== undefined) {
      setLoading(true);
      callable(e);
    }
  };

  const handleRowRender: handlerFunctionType = () => {
    if(data === undefined && loading) {
      return <Loading />;
    } else if(data === undefined) {
      return null;
    } else {
      return (data.map((player) => (
        <li className={styles.row} key={player.name}>
          <SubComponent key={player.name} {...player} />
        </li>
      )));
    }
  };

  const handleHeaderRender: handlerFunctionType = () => {
    if(data === undefined && !parentDataLoading) {
      return (
        <React.Fragment>
          <h4 key={0} className={styles.primaryHeader}>{primaryHeading[0]}</h4>
          <button type="button" className={styles.button} onClick={onClick} disabled={loading}><span>Expand</span></button>
        </React.Fragment>
      );
    } else {
      return (
        <React.Fragment>
          {primaryHeading.map((text, index) => <h4 key={index} className={styles.primaryHeader}>{text}</h4>)}
          {secondaryHeading !== undefined ? <span className={styles.secondaryHeader}>{secondaryHeading}</span> : null}
        </React.Fragment>
      );
    }
  }

  return (
    <ol className={styles.table}>
      <li className={styles.header}>
        {handleHeaderRender()}
      </li>
      {handleRowRender()}
    </ol>
  );
};

export default Table;