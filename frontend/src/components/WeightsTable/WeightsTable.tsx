import SimpleRow from "./Row/SimpleRow";
import styles from "css/WeightsTable.module.css";
import CollapsibleRow from "./Row/CollapsibleRow";
import DetailsRow from "./Row/DetailsRow";
import { IconContext } from "react-icons";


interface WeightsTableProps {
  flavor: "globalValues" | "conditionals" | "multiselects" | "shuffledSettings" | "staticSettings";
  data: any;
}

const headerTextLookup = {
  "globalValues": "Meta Settings",
  "conditionals": "Conditionals",
  "multiselects": "Multiselect Settings",
  "shuffledSettings": "Randomized Settings",
  "staticSettings": "Static Settings"
}


const WeightsTable: React.FC<WeightsTableProps> = ({ flavor, data }) => {

  const buildRow = (key: string, value: any, i: number) => {
    switch(flavor) {
      case "globalValues":
        if ((key === "tricks" || key === "disabled_locations" || key === "misc_hints") && value.length > 0) {
          return <CollapsibleRow name={key} options={value} key={i} altStyle />;
        } else { return <SimpleRow name={key} value={value} key={i} />; }
      case "conditionals":
        return <DetailsRow text={value.name} subText={value.opts} state={value.state} details={value.desc} key={i} />;
      case "multiselects":
        return <SimpleRow name={key} value={`${value}%`} key={i} />;
      case "shuffledSettings":
        return <CollapsibleRow name={key} options={value} key={i} />;
      default:
        return <SimpleRow name={key} value={value} key={i} />;
    }
  };

  return (
    <IconContext.Provider value={{ size: "1em", className: styles.iconStyle }}>
      <ul className={styles.table}>
        <li><h3>{headerTextLookup[flavor]}</h3></li>
        {
          Object.keys(data).map((key, i) => buildRow(key, data[key], i) )
        }
      </ul>
    </IconContext.Provider>





  );
};


export default WeightsTable;