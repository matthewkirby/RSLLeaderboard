// components/Table/Row/RaceResultsRow.tsx
import React from 'react';
import { getOrdinal, addPlacementClass, formatDuration } from "utils/formatting";
import styles from 'css/RaceResultRow.module.css';
import RacetimeName from 'components/RacetimeName';

interface RaceResultsData {
  place: number;
  name: string;
  discriminator: string | null;
  status: string;
  finish_time: string;
  comment: string;
  delta: number;
  ruleset: undefined | null | string;
  tertData: number;
}

const RaceResultsRow: React.FC<RaceResultsData> = (props) => {
  const isRatingGain: Boolean = props.delta > 0;
  const ordinal = getOrdinal(props.place);
  const isNonStandard = props.ruleset != null && props.ruleset.toLocaleLowerCase() !== "standard";
  const isUnscored = (props.tertData > 0) || (isNonStandard);

  const result = props.status === "dnf" ? "Forfeit" : formatDuration(props.finish_time);

  return (
    <React.Fragment>
      <span className={`${styles.placement} ${addPlacementClass(ordinal)}`}>{isNonStandard ? '' : ordinal}</span>
      <span className={styles.name}>
        <RacetimeName name={props.name} discriminator={props.discriminator} />
      </span>
      {isNonStandard
        ? <span className={styles.nonStandardRuleset}>{props.ruleset}</span>
        : null
      }
      <span className={styles.time}>{result}</span>
      <span className={`${styles.delta} ${isRatingGain ? styles.positive : styles.negative}`}>
        {isUnscored ? '' : (isRatingGain ? '+' : '') + `${Math.round(props.delta)}`}
      </span>
    </React.Fragment>
  );  
};

export default RaceResultsRow;
export type { RaceResultsData };