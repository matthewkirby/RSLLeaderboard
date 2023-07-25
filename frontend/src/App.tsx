// src/App.tsx
import React, { useState, useEffect } from 'react';
import QualifiedTable, { QualifiedPlayerData } from './components/QualifiedTable';
import UnqualifiedTable, { UnqualifiedPlayerData } from './components/UnqualifiedTable';
import styles from './App.module.css';

type LeaderboardData = {
  metadata: {
    season: number;
    datetime: string;
    required_races: number;
  };
  qualified: QualifiedPlayerData[];
  unqualified: UnqualifiedPlayerData[];
};

const App: React.FC = () => {
  const [leaderboardData, setLeaderboardData] = useState<LeaderboardData | null>(null);

  useEffect(() => {
    // Fetch data from the JSON file
    fetch('/leaderboard.json')
      .then((response) => response.json())
      .then((data) => setLeaderboardData(data));
  }, []);

  if (!leaderboardData) {
    return <div>Loading...</div>;
  }

  const lastUpdateObject = new Date(leaderboardData.metadata.datetime);
  const lastUpdateString = lastUpdateObject.toLocaleString();
  console.log(lastUpdateString)

  return (
    <div className="main">
      <QualifiedTable season={leaderboardData.metadata.season} qualifiedPlayers={leaderboardData.qualified} /><p></p>
      <UnqualifiedTable
        unqualifiedPlayers={leaderboardData.unqualified}
        requiredRaces={leaderboardData.metadata.required_races}
      /><p></p>
      <span className={styles.updateDate}>Last Updated: {lastUpdateString}</span>
    </div>
  );
};

export default App;