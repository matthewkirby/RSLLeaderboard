// src/pages/Leaderboard.tsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Table from "components/Table";
import { QualifiedPlayerData, UnqualifiedPlayerData } from 'components/Table/Row';
import LastUpdateDate from 'components/LastUpdateDate';
import Loading from 'components/Loading';

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

const Leaderboard: React.FC = () => {
  const [leaderboardData, setLeaderboardData] = useState<LeaderboardData | null>(null);

  useEffect(() => {
    axios.get(`${BASE_BACKEND_URL}/leaderboard`)
      .then((response) => setLeaderboardData(response.data))
      .catch((error) => console.error('Error fetching leaderboard data:', error));
  }, []);
  const dataSuccess = leaderboardData !== null;

  return (
    <div className="main">
      <Table
        primaryHeading={[
          dataSuccess ? `RSL Season ${leaderboardData.metadata.season}` : "Leaderboard"
        ]}
        variant="qualified"
        data={dataSuccess ? leaderboardData.qualified : undefined}
        parentDataLoading={true}
      />
      <Table
        primaryHeading={[
          "Unranked Players",
          dataSuccess ? `${leaderboardData.metadata.required_races} Total Finishes Required` : ""
        ]}
        variant="unqualified"
        data={dataSuccess ? leaderboardData.unqualified : undefined}
        parentDataLoading={true}
      />
      {dataSuccess
        ? <LastUpdateDate lastUpdateString={leaderboardData.metadata.datetime} />
        : null
      }
    </div>
  );
};

export default Leaderboard;