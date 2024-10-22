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

const formatStringParams = (template: string, params: string[], defaultParams: string[]) => {
  let formattedString = template;
  for (let i = 0; i < defaultParams.length; i++) {
    if (i < params.length) {
      formattedString = formattedString.replace('{}', params[i])
    } else {
      formattedString = formattedString.replace('{}', defaultParams[i])
    }
  }
  return formattedString;
};

const WeightsTable: React.FC<WeightsTableProps> = ({ flavor, data, override }) => {

  const buildRow = (key: string, baseValue: any, i: number) => {
    const value = override?.[key] ?? baseValue;
    const trueState = override[value.id]?.[0] ?? baseValue.state;
    let isOverridden = false;
    if (flavor === "conditionals") {
      if (value.id in override) {
        isOverridden = true;
      }
    } else if (key in override) {
      isOverridden = true;
    }


    switch(flavor) {
      case "globalValues":
        if ((key === "tricks" || key === "disabled_locations" || key === "misc_hints") && value.length > 0) {
          return <CollapsibleRow name={key} options={value} isOverridden={isOverridden} altStyle key={i} />;
        } else { return <SimpleRow name={key} value={value} isOverridden={isOverridden} key={i} />; }
      case "conditionals":
        let condParams = isOverridden ? override[value.id].slice(1) : value.defaults;
        const subText = formatStringParams(value.optstr, condParams, value.defaults);
        const fullDesc = formatStringParams(value.desc, condParams, value.defaults);
        return <DetailsRow text={value.name} subText={subText} state={trueState} details={fullDesc} isOverridden={isOverridden} key={i} />;
      case "multiselects":
        return <SimpleRow name={key} value={`${value}%`} isOverridden={isOverridden} key={i} />;
      case "shuffledSettings":
        if (Object.values(value as WeightType).reduce((partial, a) => partial + a, 0) > 1) {
          return <CollapsibleRow name={key} options={value} isOverridden={isOverridden} key={i} />;
        } else {
          return "";
        }
      case "staticSettings":
        if (Object.values(value as WeightType).reduce((partial, a) => partial + a, 0) < 1.5) {
          const soloValue = Object.keys(value).find(key => value[key] > 0);
          return <SimpleRow name={key} value={soloValue as string} isOverridden={isOverridden} key={i} />;
        } else {
          return "";
        }
      default:
        return <SimpleRow name={key} value={value} key={i} isOverridden={isOverridden} />;
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