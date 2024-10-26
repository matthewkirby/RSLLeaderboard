// src/pages/RaceHistory.tsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Table from "components/Table";
import { RaceResultsData } from 'components/Table/Row';
import { formatDatetime, seasonFormatting } from 'utils/formatting';
import { reportApiError } from 'utils/api';

interface RaceData {
  slug: string,
  ended_at: string,
  season: string,
  url: string
};

interface RaceEntrantData {
  [key: string]: RaceResultsData[]
};

const BASE_BACKEND_URL = process.env.REACT_APP_BACKEND_ROOT;

const formatRASlugs = (slug: string) => {
  if (slug.split('-')[0] === "season")
    return slug.split('-').slice(2).join('-');
  else
    return slug;
};

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
      .catch((error) => reportApiError(error));
  }, []);
  const dataSuccess = racelist !== null;


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
      .catch((error) => reportApiError(error));
  };

  return (
    <>
      {dataSuccess
        ? racelist.map((race, index) => {
          return (
            <Table
              key={index}
              primaryHeading={[formatRASlugs(race.slug)]}
              secondaryHeading={[`(${seasonFormatting(race.season)})`, formatDatetime(race.ended_at)]}
              variant={"raceResults"}
              data={raceEntrants[race.slug]}
              callable={() => getRaceEntrantData(race.slug)}
              url={race.url}
            />
          );
        })
        : [0,1,2,3,4].map((index) => {
          return (
            <Table
              key={index}
              primaryHeading={[`Race Name Placeholder ${index+1}`]}
              variant={"raceResults"}
              data={undefined}
              parentDataLoading={true}
            />
          );
        })
      }
    </>
  );
}

export default RaceHistory;