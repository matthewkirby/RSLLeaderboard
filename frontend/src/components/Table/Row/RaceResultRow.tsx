// components/Table/Row/RaceResultsRow.tsx
import React from 'react';
import { getOrdinal, addPlacementClass, formatDuration } from "utils/formatting";
import styles from 'css/RaceResultRow.module.css';
import RacetimeName from 'components/RacetimeName';

interface RaceResultsData {
  place: number,
  name: string,
  discriminator: string | null,
  status: string,
  finish_time: string,
  comment: string,
  delta: number
}

const RaceResultsRow: React.FC<RaceResultsData> = (props) => {
  const isRatingGain: Boolean = props.delta > 0;
  const ordinal = getOrdinal(props.place);

  let result: string = "";
  if (props.status === "dnf") {
    result = "Forfeit";
  } else {
    result = formatDuration(props.finish_time);
  }

  return (
    <React.Fragment>
      <span className={`${styles.placement} ${addPlacementClass(ordinal)}`}>{ordinal}</span>
      <span className={styles.name}>
        <RacetimeName name={props.name} discriminator={props.discriminator} />
      </span>
      {/* <span className={styles.comment}></span> */}
      <span className={styles.time}>{result}</span>
      <span className={`${styles.delta} ${isRatingGain ? styles.positive : styles.negative}`}>
        {(isRatingGain ? '+' : '') + `${Math.round(props.delta)}`}
      </span>
    </React.Fragment>
  );  
};

export default RaceResultsRow;
export type { RaceResultsData };