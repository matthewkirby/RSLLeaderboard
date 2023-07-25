// components/UnqualifiedTable.tsx
import React from 'react';
import styles from './UnqualifiedTable.module.css';

type UnqualifiedPlayerData = {
  name: string;
  entries: number;
  finishes: number;
  rating: number;
};

type UnqualifiedTableProps = {
  unqualifiedPlayers: UnqualifiedPlayerData[];
  requiredRaces: number;
};

const UnqualifiedTable: React.FC<UnqualifiedTableProps> = ({ unqualifiedPlayers, requiredRaces }) => {
  return (
    <ol className="table">
      <li className="header">
        <h4>Unranked Players</h4>
        <h4>3 Total Finishes Required</h4>
      </li>
      {unqualifiedPlayers.map((player) => {
        return (
          <li className="body" key={player.name}>
            <span className={styles.unrankedName}>{player.name}</span>
            <span className={styles.unrankedRemaining}>
              {requiredRaces-player.finishes} more finishes to qualify.
            </span>
          </li>
        )})}
    </ol>
  );
};

export default UnqualifiedTable;
export type { UnqualifiedPlayerData };