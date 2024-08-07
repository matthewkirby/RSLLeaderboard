// src/App.tsx
import React from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import Leaderboard from 'pages/Leaderboard';
import RaceHistory from 'pages/RaceHistory';
import NavBar from 'components/NavBar';
import Weights from 'pages/Weights';

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={ <NavBar /> }>
        <Route index element={ <Leaderboard /> } />
        <Route path="races" element={ <RaceHistory /> } />
        <Route path="weights" element={ <Weights /> } />
        <Route path="*" element={ <Navigate to="/" /> } />
      </Route>
    </Routes>
  );
};

export default App;