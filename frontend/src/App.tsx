// src/App.tsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Table from "./components/Table";
import styles from './App.module.css';
import { QualifiedPlayerData, UnqualifiedPlayerData } from 'components/Table/Row';

type LeaderboardData = {
  metadata: {
    season: number;
    datetime: string;
    required_races: number;
  };
  qualified: QualifiedPlayerData[];
  unqualified: UnqualifiedPlayerData[];
};

const BASE_BACKEND_URL = 'http://localhost:5000/api';

const App: React.FC = () => {
  const [leaderboardData, setLeaderboardData] = useState<LeaderboardData | null>(null);

  useEffect(() => {
    axios.get(`${BASE_BACKEND_URL}/leaderboard`)
      .then((response) => setLeaderboardData(response.data))
      .catch((error) => console.error('Error fetching leaderboard data:', error));
  }, []);

  if (!leaderboardData) {
    return <div>Loading...</div>;
  }

  const lastUpdateObject = new Date(leaderboardData.metadata.datetime);
  const lastUpdateString = lastUpdateObject.toLocaleString([], {dateStyle: 'medium', timeStyle: 'long'});
  console.log(lastUpdateString)

  return (
    <div className="main">
      <Table
        primaryHeading={[
          `RSL Season ${leaderboardData.metadata.season}`
        ]}
        variant="qualified"
        data={leaderboardData.qualified}
      /><p></p>
      <Table
        primaryHeading={[
          "Unranked Players",
          `${leaderboardData.metadata.required_races} Total Finishes Required`
        ]}
        variant="unqualified"
        data={leaderboardData.unqualified}
      /><p></p>
      <span className={styles.updateDate}>Last Updated: {lastUpdateString}</span>
    </div>
  );
};

export default App;