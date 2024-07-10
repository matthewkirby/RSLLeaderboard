interface SimpleRowProps {
  name: string;
  value: string | boolean | number | string[];
  isOverridden?: boolean;
}


const formatDisplayValue = (value: string | boolean | number | string[]) => {
  switch (typeof(value)) {
    case ("boolean"):
      if (value) {
        return "Enabled";
      } else {
        return "Disabled";
      }

    case ("number"):
      return String(value);

    case ("string"):
      return value;
    
    case ("object"):
      if ((value as string[]).length === 0) {
        return "None";
      } else {
        return (value as string[]).reduce((acc, curr) => acc += `, ${curr}`, "");
      }
  }
};


const SimpleRow: React.FC<SimpleRowProps> = ({ name, value, isOverridden = false }) => {
  return (
    <li style={isOverridden ? {backgroundColor: "#102a43"} : {}}>
      <span>
        <h4>{name}</h4>
      </span>
      <span>
        {formatDisplayValue(value)}
      </span>
    </li>
  );
};

export default SimpleRow;