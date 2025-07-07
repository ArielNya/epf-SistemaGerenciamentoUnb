import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router';
import Navbar from './components/Navbar';
import Home from './pages/Home'; 
import Alunos from './pages/Alunos'; 
import MatricularDesmatricular from './pages/MatricularDesmatricular'; 
import Disciplinas from './pages/Diciplinas';


function App() {
  return (
    <Router>
      <Navbar />
      <div style={{ padding: '20px' }}> 
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/alunos" element={<Alunos />} />
          <Route path="/alunos/matricular-desmatricular/:matricula" element={<MatricularDesmatricular />} />
           <Route path="/disciplinas" element={<Disciplinas />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;