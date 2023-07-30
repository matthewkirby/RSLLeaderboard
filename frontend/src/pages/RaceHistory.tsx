// src/pages/RaceHistory.tsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Table from "components/Table";
import { RaceResultsData } from 'components/Table/Row';
import { formatDatetime } from 'utils/formatting';
import Loading from 'components/Loading';

interface RaceData {
  slug: string,
  ended_at: string,
  season: number,
  url: string
};

interface RaceHistoryData {
  racelist: RaceData[],
  entrants: {
    [key: string]: RaceResultsData[]
  }
};

const BASE_BACKEND_URL = 'http://localhost:5000/api';

const RaceHistory: React.FC = () => {
  const [raceHistoryData, setRaceHistoryData] = useState<RaceHistoryData | null>(null);

  useEffect(() => {
    axios.get(`${BASE_BACKEND_URL}/racelist`)
      .then((response) => setRaceHistoryData(response.data))
      .catch((error) => console.error('Error fetching historic race data:', error));
  }, []);

  if (raceHistoryData === null) {
    return <Loading />;
  }

  return (
    <div className="main">
      {raceHistoryData.racelist.map((race, index) => {
        return (
          <Table
            key={index}
            primaryHeading={[race.slug]}
            secondaryHeading={formatDatetime(race.ended_at)}
            variant={"raceResults"}
            data={raceHistoryData.entrants[race.slug]}
          />
        );
      })};
    </div>
  );
}

export default RaceHistory;