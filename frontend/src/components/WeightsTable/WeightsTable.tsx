import SimpleRow from "./Row/SimpleRow";
import styles from "css/WeightsTable.module.css";
import CollapsibleRow from "./Row/CollapsibleRow";
import DetailsRow from "./Row/DetailsRow";
import { IconContext } from "react-icons";


interface WeightsTableProps {
  flavor: "globalValues" | "conditionals" | "multiselects" | "shuffledSettings" | "staticSettings";
  data: any;
  override?: any;
}

type WeightType = { [key:string]: number };

const headerTextLookup = {
  "globalValues": "Meta Settings",
  "conditionals": "Conditionals",
  "multiselects": "Multiselect Settings",
  "shuffledSettings": "Randomized Settings",
  "staticSettings": "Static Settings"
}


const WeightsTable: React.FC<WeightsTableProps> = ({ flavor, data, override }) => {

  const buildRow = (key: string, basevalue: any, i: number) => {
    const value = override?.[key] ?? basevalue;
    switch(flavor) {
      case "globalValues":
        if ((key === "tricks" || key === "disabled_locations" || key === "misc_hints") && value.length > 0) {
          return <CollapsibleRow name={key} options={value} key={i} altStyle />;
        } else { return <SimpleRow name={key} value={value} key={i} />; }
      case "conditionals":
        const trueState = override[value.id]?.[0] ?? basevalue.state;
        return <DetailsRow text={value.name} subText={value.opts} state={trueState} details={value.desc} key={i} />;
      case "multiselects":
        return <SimpleRow name={key} value={`${value}%`} key={i} />;
      case "shuffledSettings":
        if (Object.values(value as WeightType).reduce((partial, a) => partial + a, 0) > 1) {
          return <CollapsibleRow name={key} options={value} key={i} />;
        } else {
          return "";
        }
      case "staticSettings":
        if (Object.values(value as WeightType).reduce((partial, a) => partial + a, 0) < 1.5) {
          const soloValue = Object.keys(value).find(key => value[key] > 0);
          return <SimpleRow name={key} value={soloValue as string} key={i} />;
        } else {
          return "";
        }
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