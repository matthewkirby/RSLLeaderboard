// src/pages/Weights.tsx
import axios from 'axios';
import MultiStateButton from 'components/MultiStateButton';
import React, { useEffect, useState } from 'react';
import { reportApiError } from 'utils/api';
import WeightsTable from 'components/WeightsTable/WeightsTable';


const buttonStates = ["rsl", "lite", "intermediate"];
const BASE_BACKEND_URL = process.env.REACT_APP_BACKEND_ROOT;

type WeightsData = {
  global_settings: { [key:string]: string | number | boolean };
  conditionals: { [key:string]: string | number | boolean };
  multiselects: { [key:string]: string | number | boolean };
  weights: { [key:string]: { [key:string]: number } };
  overrides: {
    beginner: { [key:string]: string | number | boolean };
    intermediate: { [key:string]: string | number | boolean };
  }
};


const Weights: React.FC = () => {

  const [preset, setPreset] = useState(0);
  const [weightsData, setWeightsData] = useState<WeightsData|null>(null);

  useEffect(() => {
    axios.get(`${BASE_BACKEND_URL}/weights`)
      .then((response) => setWeightsData(response.data))
      .catch((error) => reportApiError(error));
  }, []);
  const dataSuccess = weightsData !== null;

  let override = {};
  if (dataSuccess) {
    if (preset === 1) {
      override = weightsData["overrides"]["beginner"];
    } else if (preset === 2) {
      override = weightsData["overrides"]["intermediate"];
    }
  }


  return (
    <>
      <div style={{"display": "flex", "width": "100%", "justifyContent": "center"}}>
        <MultiStateButton
          buttonLabels={buttonStates}
          activeIndex={preset}
          onClick={setPreset}
        />
      </div>
      {dataSuccess ? <>
      <WeightsTable
        flavor="globalValues"
        data={weightsData.global_settings}
        override={override}
      />
      <WeightsTable
        flavor="conditionals"
        data={weightsData.conditionals}
        override={override}
      />
      <WeightsTable
        flavor="multiselects"
        data={weightsData.multiselects}
        override={override}
      />
      <WeightsTable
        flavor="shuffledSettings"
        data={weightsData.weights}
        override={override}
      />
      <WeightsTable
        flavor="staticSettings"
        data={weightsData.weights}
        override={override}
      />
      </> : ""}
    </>
  );
};

export default Weights;