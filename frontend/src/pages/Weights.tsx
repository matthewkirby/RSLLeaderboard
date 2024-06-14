// src/pages/Weights.tsx
import MultiStateButton from 'components/MultiStateButton';
import React, { useState } from 'react';


const buttonStates = ["rsl", "beginner", "intermediate"];


const Weights: React.FC = () => {

  const [preset, setPreset] = useState(0)

  return (
    <>
      <div style={{"display": "flex", "width": "100%", "justifyContent": "center"}}>
        <MultiStateButton
          buttonLabels={buttonStates}
          activeIndex={preset}
          onClick={setPreset}
        />
      </div>
    </>
  );
};

export default Weights;