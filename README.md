# Physics Simulations Lab 🎓

A full-stack application for interactive visualization of classical mechanics simulations. Built with FastAPI backend and React frontend.

## Features

### 🎯 Three Physics Simulations

1. **Free Fall** - Bouncing ball with gravity and energy damping
2. **Pendulum** - Simple pendulum motion with optional damping
3. **Projectile** - Projectile motion with air resistance

### 💻 Technology Stack

- **Backend**: FastAPI + Uvicorn + NumPy + SciPy
- **Frontend**: React 18 + Chart.js + Axios
- **Container**: Docker & Docker Compose
- **Physics**: ODE integration via scipy.integrate.odeint

## Quick Start

### Option 1: Local Development

#### Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run server
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Docker Compose

```bash
docker-compose up --build
```

## Project Structure

```
FreeFall/
├── physics_simulations/     # Core physics modules
│   ├── free_fall.py        # Free fall simulation
│   ├── pendulum.py         # Pendulum simulation
│   └── projectile.py       # Projectile simulation
├── backend/                # FastAPI application
│   ├── main.py            # API endpoints
│   └── requirements.txt
├── frontend/              # React application
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
└── IMPLEMENTATION_PLAN.md
```

## API Endpoints

### Free Fall
- `POST /api/simulate/free-fall`
- `GET /api/simulate/free-fall/defaults`

### Pendulum
- `POST /api/simulate/pendulum`
- `GET /api/simulate/pendulum/defaults`

### Projectile
- `POST /api/simulate/projectile`
- `GET /api/simulate/projectile/defaults`

## Documentation

See `IMPLEMENTATION_PLAN.md` for comprehensive documentation including:
- Detailed physics equations
- API usage examples
- Development guidelines
- Extension ideas

## License

MIT License
