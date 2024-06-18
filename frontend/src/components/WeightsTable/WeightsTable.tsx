import SimpleRow from "./Row/SimpleRow";
import styles from "css/WeightsTable.module.css";


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
        return <SimpleRow name={key} value={value} key={i} />
      case "conditionals":
        return <></>;
      case "multiselects":
        return <></>;
    }
  };

  return (
    <ul className={styles.table}>
      <li><h3>{headerTextLookup[flavor]}</h3></li>
      {
        Object.keys(data).map((key, i) => buildRow(key, data[key], i) )
      }
    </ul>





  );
};


export default WeightsTable;