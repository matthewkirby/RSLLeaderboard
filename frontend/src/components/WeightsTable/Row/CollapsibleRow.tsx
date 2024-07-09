import styles from "css/WeightsTable.module.css";
import { useState } from "react";
import { FaAngleDown, FaAngleRight } from "react-icons/fa6";


interface CollapsibleRowProps {
  name: string;
  options: { [key: string]: number };
  altStyle?: boolean;
}


const CollapsibleRow: React.FC<CollapsibleRowProps> = ({ name, options, altStyle}) => {
  const [isVisible, setIsVisible] = useState<boolean>(true);
  const totalWeight = Object.values(options).reduce((a, b) => a + b, 0);

  return (
    <li className={styles.crow} onClick={() => setIsVisible(!isVisible)}>
      <div className={styles.settingName}>
        <h4>{isVisible ? <FaAngleDown /> : <FaAngleRight />} {name}</h4>
      </div>
      <div style={isVisible ? {} : {display: "none"}} className={styles.optionBlock}>
        {Object.keys(options).map((opt, i) => {
          const perc = 100*options[opt]/totalWeight;
          return (
            <div key={i}>
              {altStyle ?
                <span>
                  {`${options[opt]}`}
                </span>
              :
                <>
                  <span className={styles.optionWeight}>
                    {`${perc.toPrecision(3).replace(/\.?0+$/,"")}%`}
                  </span>
                  <span>
                    {`${opt}`}
                  </span>
                </>
              }
            </div>
          );
        })}
      </div>
    </li>
  );
};

CollapsibleRow.defaultProps = {
  altStyle: false
};

export default CollapsibleRow;