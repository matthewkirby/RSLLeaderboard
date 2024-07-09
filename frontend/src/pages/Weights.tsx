// src/pages/Weights.tsx
import axios from 'axios';
import MultiStateButton from 'components/MultiStateButton';
import React, { useEffect, useState } from 'react';
import { reportApiError } from 'utils/api';
import WeightsTable from 'components/WeightsTable/WeightsTable';


const buttonStates = ["rsl", "beginner", "intermediate"];
const BASE_BACKEND_URL = process.env.REACT_APP_BACKEND_ROOT;

type WeightsData = {
  global_settings: { [key:string]: string | number | boolean };
  conditionals: { [key:string]: string | number | boolean };
  multiselects: { [key:string]: string | number | boolean };
  randomized: { [key:string]: string | number | boolean };
  static: { [key:string]: string | number | boolean };
};


const Weights: React.FC = () => {

  const [preset, setPreset] = useState(0)
  const [weightsData, setWeightsData] = useState<WeightsData|null>(null)

  useEffect(() => {
    axios.get(`${BASE_BACKEND_URL}/weights`)
      .then((response) => setWeightsData(response.data))
      .catch((error) => reportApiError(error));
  }, []);
  const dataSuccess = weightsData !== null;


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
      />
      <WeightsTable
        flavor="conditionals"
        data={{}}
      />
      <WeightsTable
        flavor="multiselects"
        data={{}}
      />
      <WeightsTable
        flavor="shuffledSettings"
        data={weightsData.randomized}
      />
      <WeightsTable
        flavor="staticSettings"
        data={weightsData.static}
      />
      </> : ""}
    </>
  );
};

export default Weights;