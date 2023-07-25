// components/QualifiedTable.tsx
import React from 'react';
import styles from './QualifiedTable.module.css';

function getOrdinal(number: number): string {
  const suffixes = ['th', 'st', 'nd', 'rd'];
  const v = number % 100;
  return number + (suffixes[(v - 20) % 10] || suffixes[v] || suffixes[0]);
};

function addPlacementClass(ordinal: string): string {
  if (ordinal === "1st") {
    return styles.firstPlace;
  } else if (ordinal === "2nd") {
    return styles.secondPlace;
  } else if (ordinal === "3rd") {
    return styles.thirdPlace;
  } else {
    return "";
  }
};

type QualifiedPlayerData = {
  name: string;
  entries: number;
  finishes: number;
  rating: number;
  placement: number;
};

type QualifiedTableProps = {
  season: number;
  qualifiedPlayers: QualifiedPlayerData[];
};

const QualifiedTable: React.FC<QualifiedTableProps> = ({ season, qualifiedPlayers }) => {
  return (
    <ol className="table">
      <li className="header">
        <h4>RSL Season {season}</h4>
      </li>
      {qualifiedPlayers.map((player) => {
        const ordinal = getOrdinal(player.placement);
      return (
        <li className="body" key={player.name}>
          <span className={`${styles.placement} ${addPlacementClass(ordinal)}`}>{ordinal}</span>
          <span className={styles.name}>{player.name}</span>
          <span className={styles.rating}>{player.rating}</span>
          <span className={styles.extraData}>
            <span className={styles.finishes}>{player.finishes} Finishes</span>
            <span className={styles.entries}>{player.entries} Races</span>
          </span>
        </li>
      )})}
    </ol>
  );
};

export default QualifiedTable;
export type { QualifiedPlayerData };