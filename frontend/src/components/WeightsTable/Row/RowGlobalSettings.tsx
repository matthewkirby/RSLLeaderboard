interface RowGlobalSettingsProps {
  name: string;
  value: string | boolean | number | string[];
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


const RowGlobalSettings: React.FC<RowGlobalSettingsProps> = ({ name, value }) => {

  return (
    <li>
      <span>
        <h4>{name}</h4>
      </span>
      <span>
        {formatDisplayValue(value)}
      </span>
    </li>
  );
};

export default RowGlobalSettings;