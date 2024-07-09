import styles from "css/WeightsTable.module.css";
import { useState } from "react";
import { IconContext } from "react-icons";
import { FaAngleDown, FaAngleRight } from "react-icons/fa6";


interface CollapsibleRowProps {
  name: string;
  options: { [key: string]: number };
}


const CollapsibleRow: React.FC<CollapsibleRowProps> = ({ name, options }) => {
  const [isVisible, setIsVisible] = useState<boolean>(true);
  const totalWeight = Object.values(options).reduce((a, b) => a + b, 0);

  return (
    <IconContext.Provider value={{ size: "1em", className: styles.iconStyle }}>
      <li className={styles.crow} onClick={() => setIsVisible(!isVisible)}>
        <div className={styles.settingName}>
          <h4>{isVisible ? <FaAngleDown /> : <FaAngleRight />} {name}</h4>
        </div>
        <div style={isVisible ? {} : {display: "none"}} className={styles.optionBlock}>
          {Object.keys(options).map((opt, i) => {
            const perc = 100*options[opt]/totalWeight;
            return (
              <div key={i}>
                <span className={styles.optionWeight}>
                  {`${perc.toPrecision(3).replace(/\.?0+$/,"")}%`}
                </span>
                <span>
                  {`${opt}`}
                </span>
              </div>
            );
          })}
        </div>
      </li>
    </IconContext.Provider>
  );
};

export default CollapsibleRow;