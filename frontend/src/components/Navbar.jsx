// src/components/Navbar.jsx
import React from 'react';
import { Link } from 'react-router';

const Navbar = () => {
  return (
    <nav style={{ backgroundColor: '#333', padding: '10px 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <Link to="/" style={{ color: 'white', textDecoration: 'none', fontSize: '1.5em', fontWeight: 'bold' }}>
        Sistema Escolar
      </Link>
      <div>
        <ul style={{ listStyle: 'none', margin: 0, padding: 0, display: 'flex' }}>
          <li style={{ marginLeft: '20px' }}>
            <Link to="/alunos" style={{ color: 'white', textDecoration: 'none', fontSize: '1.1em' }}>
              Alunos
            </Link>
          </li>
          <li style={{ marginLeft: '20px' }}>
            <Link to="/disciplinas" style={{ color: 'white', textDecoration: 'none', fontSize: '1.1em' }}>
              Disciplinas
            </Link>
          </li>
          <li style={{ marginLeft: '20px' }}>
            <Link to="/turmas" style={{ color: 'white', textDecoration: 'none', fontSize: '1.1em' }}>
              Turmas
            </Link>
          </li>
          <li style={{ marginLeft: '20px' }}>
            <Link to="/notas-frequencias" style={{ color: 'white', textDecoration: 'none', fontSize: '1.1em' }}>
              Notas/Frequências
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;