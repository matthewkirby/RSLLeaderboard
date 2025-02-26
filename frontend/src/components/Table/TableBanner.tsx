// components/Table/TableBanner.tsx
import styles from 'css/TableBanner.module.css';
import React from 'react';

type messageTableType = {[key: string]: string}
interface TableBannerProps {
  flag: number;
};

const messageTable: messageTableType = {
  1: "Race not scored: Not publicly announced",
  2: ""
}

const TableBanner: React.FC<TableBannerProps> = ({ flag }) => {

  const bgColor
    = flag === 1 ? styles.bannerRed
    : flag === 2 ? styles.bannerBlue
    : null;

  if (bgColor === null) { return null; }

  return (
    <li className={`${styles.tableBanner} ${bgColor}`}>
      {messageTable[flag]}
    </li>
  );
};

export default TableBanner;