import { FaAngleDown, FaAngleRight } from "react-icons/fa6";
import styles from "css/DetailsRow.module.css";
import { useState } from "react";


interface DetailsRowProps {
  text: string;
  subText: string;
  state: boolean;
  details: string;
  startsExpanded?: boolean;
  isOverridden?: boolean;
}


const DetailsRow: React.FC<DetailsRowProps> = ({ text, subText, state, details, startsExpanded = false, isOverridden = false }) => {
  const [isExpanded, setIsExpanded] = useState<boolean>(startsExpanded);

  let formattedText = text.toLowerCase().split(' ')
    .map((s) => s === "mq" ? "MQ" : s)
    .map((s) => s.charAt(0).toUpperCase() + s.substring(1))
    .join(' ');

  return (
    // DONE INLINE BECAUSE SPECIFICITY. IMPROVE CSS DEFINITIONS TO FIX THIS
    <li style={isOverridden ? {flexDirection: "column", padding: "0", backgroundColor: "#102a43"} : {flexDirection: "column", padding: "0"}}
      onClick={() => setIsExpanded(!isExpanded)}
      className={styles.detailsRow}
    >
      <div className={styles.detailsHeader}>
        <h4>{isExpanded ? <FaAngleDown /> : <FaAngleRight />}</h4>
        <h4 className={state ? "" : styles.disabledText}>{formattedText}</h4>
        {isExpanded ? <></> : state ?
          <h5 className={styles.subText}>{subText}</h5> :
          <h5 className={styles.disabledText}>Disabled</h5>
        }
      </div>
      <div className={styles.detailsBody} style={isExpanded ? {} : {display: "none"}}>
        {state ? <></> : <h4 className={styles.disabledText}>! This conditional is DISABLED !</h4>}
        <p>{details}</p>
      </div>
    </li>
  );
};


export default DetailsRow;