import React, { useState } from 'react';
import './App.css';
import FreeFallSimulator from './components/FreeFallSimulator';
import PendulumSimulator from './components/PendulumSimulator';
import ProjectileSimulator from './components/ProjectileSimulator';

function App() {
  const [activeSimulation, setActiveSimulation] = useState('free-fall');

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🎓 Physics Simulations Lab</h1>
        <p>Interactive visualization of classical mechanics</p>
      </header>

      <nav className="simulation-nav">
        <button
          className={`nav-button ${activeSimulation === 'free-fall' ? 'active' : ''}`}
          onClick={() => setActiveSimulation('free-fall')}
        >
          📉 Free Fall
        </button>
        <button
          className={`nav-button ${activeSimulation === 'pendulum' ? 'active' : ''}`}
          onClick={() => setActiveSimulation('pendulum')}
        >
          ⏰ Pendulum
        </button>
        <button
          className={`nav-button ${activeSimulation === 'projectile' ? 'active' : ''}`}
          onClick={() => setActiveSimulation('projectile')}
        >
          🚀 Projectile
        </button>
      </nav>

      <main className="app-content">
        {activeSimulation === 'free-fall' && <FreeFallSimulator />}
        {activeSimulation === 'pendulum' && <PendulumSimulator />}
        {activeSimulation === 'projectile' && <ProjectileSimulator />}
      </main>

      <footer className="app-footer">
        <p>Physics Simulations Lab v1.0.0 | Built with React + FastAPI</p>
      </footer>
    </div>
  );
}

export default App;
