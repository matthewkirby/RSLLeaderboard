// components/Table/Row/index.ts
import React from "react";
import QualifiedRow, { QualifiedPlayerData } from "./QualifiedRow";
import UnqualifiedRow, { UnqualifiedPlayerData } from "./UnqualifiedRow";

export type TableVariants = "qualified" | "unqualified";// | "race_results";
export type DataVariants = QualifiedPlayerData | UnqualifiedPlayerData;

// I am using any here which is bad. I spent hours and could not resolve the issue.
// The problem is that I want to say that the value has to be one of DataVariants
// But then the components say they can only be one of those. So I get an error that
// says something like QualifiedRow can't take props of type UnqualifiedPlayerData.
// The best fix is probably to do something where I determine which component to use
// by the type of the data. So if my data was type UnqualifiedPlayerData, I use
// UnqualifiedRow etc. For now, I am just going to leave it like this.
const rowComponents: Record<TableVariants, React.FC<any>> = {
  qualified: QualifiedRow,
  unqualified: UnqualifiedRow,
  // race_results: null
};

export default rowComponents;
export type { QualifiedPlayerData, UnqualifiedPlayerData };