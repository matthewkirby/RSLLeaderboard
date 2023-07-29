// components/LastUpdateDate.tsx
import React from 'react';

const stylesContainer: React.CSSProperties = {
  flexBasis: "100%",
  margin: "0 0 var(--gap) 0",
};

const stylesText: React.CSSProperties = {
  width: "var(--element-primary-width)",
  display: "flex",
  justifyContent: "space-evenly"
}

interface LastUpdateDateProps {
  lastUpdateString: string
}

const LastUpdateDate: React.FC<LastUpdateDateProps> = ({ lastUpdateString }) => {
  return (
    <span style={stylesContainer}>
      <span style={stylesText}>
        Last Updated: {lastUpdateString}
      </span>
    </span>
  );
};

export default LastUpdateDate;