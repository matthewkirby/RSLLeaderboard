// components/Table/Table.tsx
import React, { useState } from 'react';
import styles from 'css/Table.module.css';
import rowComponents, { DataVariants, TableVariants } from './Row';
import Loading from 'components/Loading';

type handlerFunctionType = () => React.ReactNode;


interface LinkWrapperProps {
  url?: string | null;
  children: React.ReactNode;
}

const LinkWrapper: React.FC<LinkWrapperProps> = ({ url, children }) => {
  if(url)
    return <a href={`https://www.racetime.gg${url}`} className={styles.rtlink} target="_blank" rel="noreferrer">{children}</a>;
  return <>{children}</>
}

interface TableProps {
  primaryHeading: string[];
  secondaryHeading?: string[];
  variant: TableVariants;
  data: DataVariants[] | undefined;
  parentDataLoading?: boolean;
  callable?: React.MouseEventHandler<HTMLButtonElement>;
  url?: string | null;
}

const Table: React.FC<TableProps> = ({ primaryHeading, secondaryHeading, variant, data, parentDataLoading, callable, url}) => {
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
          <LinkWrapper url={url}>
            <h4 className={styles.primaryHeader}>{primaryHeading[0]}</h4>
          </LinkWrapper>
          {secondaryHeading !== undefined  ? <span className={styles.secondaryHeader}>{secondaryHeading[0]}</span> : null}
          <button type="button" className={styles.button} onClick={onClick} disabled={loading}><span>Expand</span></button>
        </React.Fragment>
      );
    } else {
      return (
        <React.Fragment>
          <LinkWrapper url={url}>
            {primaryHeading.map((text, index) => <h4 key={index} className={styles.primaryHeader}>{text}</h4>)}
          </LinkWrapper>
          {secondaryHeading !== undefined
            ? secondaryHeading.map((text, index) => <span key={index} className={styles.secondaryHeader}>{text}</span>)
            : null
          }
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