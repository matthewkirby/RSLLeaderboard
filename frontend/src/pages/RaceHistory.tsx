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

interface RaceEntrantData {
  [key: string]: RaceResultsData[]
};

const BASE_BACKEND_URL = 'http://localhost:5000/api';

const RaceHistory: React.FC = () => {
  const [racelist, setRacelist] = useState<RaceData[] | null>(null);
  const [raceEntrants, setRaceEntrants] = useState<RaceEntrantData>(() => {
    const storedData: string | null = localStorage.getItem("raceEntrants");
    return JSON.parse(storedData ?? "{}");
  });

  // Make API request for the racelist and 5 most recent races
  useEffect(() => {
    axios.get(`${BASE_BACKEND_URL}/racelist`)
      .then((response) => { 
        setRacelist(response.data.racelist);
        setRaceEntrants((prevRaceEntrants) => ({
          ...prevRaceEntrants,
          ...response.data.entrants
        }));
      })
      .catch((error) => console.error('Error fetching historic race data:', error));
  }, []);

  // If raceEntrants changes, save to localstorage
  useEffect(() => {
    localStorage.setItem('raceEntrants', JSON.stringify(raceEntrants))
  }, [raceEntrants]);

  // Get race entrants for a single race
  function getRaceEntrantData(slug: string): void {
    axios.get(`${BASE_BACKEND_URL}/race_entrants?slug=${slug}`)
      .then((response) => {
        setRaceEntrants((prevRaceEntrants) => ({
          ...prevRaceEntrants,
          ...response.data
        }));
      })
      .catch((error) => console.error(`Error fetching entrant data for ${slug}:`, error));
  };

  if (racelist === null) {
    return <Loading />;
  }

  return (
    <div className="main">
      {racelist.map((race, index) => {
        return (
          <Table
            key={index}
            primaryHeading={[race.slug]}
            secondaryHeading={formatDatetime(race.ended_at)}
            variant={"raceResults"}
            data={raceEntrants[race.slug]}
            callable={() => getRaceEntrantData(race.slug)}
          />
        );
      })}
    </div>
  );
}

export default RaceHistory;