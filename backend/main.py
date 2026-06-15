"""
FastAPI Backend for Physics Simulations
REST API endpoints for free fall, pendulum, and projectile motion simulations.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics_simulations.free_fall import FreeFallSimulation
from physics_simulations.pendulum import PendulumSimulation
from physics_simulations.projectile import ProjectileSimulation

app = FastAPI(
    title="Physics Simulations API",
    description="API for computing physics trajectories",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class FreeFallRequest(BaseModel):
    initial_height: float = 10.0
    gravity: float = 9.81
    bounce_damping: float = 0.8
    num_bounces: int = 4


class FreeFallResponse(BaseModel):
    x_positions: list
    y_positions: list
    dt: float
    initial_height: float
    gravity: float
    radius: float
    bounce_damping: float
    num_bounces: int


class PendulumRequest(BaseModel):
    length: float = 1.0
    gravity: float = 9.81
    damping: float = 0.1
    initial_angle: float = 0.785  # π/4 in radians
    time_duration: float = 20.0


class PendulumResponse(BaseModel):
    x_positions: list
    y_positions: list
    angles: list
    times: list
    dt: float
    length: float
    gravity: float
    damping: float
    initial_angle: float


class ProjectileRequest(BaseModel):
    initial_velocity: float = 20.0
    launch_angle: float = 45.0
    gravity: float = 9.81
    air_resistance: float = 0.0
    mass: float = 1.0


class ProjectileResponse(BaseModel):
    x_positions: list
    y_positions: list
    vx_positions: list
    vy_positions: list
    dt: float
    initial_velocity: float
    launch_angle: float
    gravity: float
    air_resistance: float
    max_height: float
    range: float


# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "physics-simulations"}


# Free Fall Endpoints
@app.post("/api/simulate/free-fall", response_model=FreeFallResponse)
async def simulate_free_fall(request: FreeFallRequest):
    """
    Simulate free fall with bouncing.
    
    Parameters:
    - initial_height: Starting height in meters (default: 10.0)
    - gravity: Acceleration due to gravity (default: 9.81 m/s²)
    - bounce_damping: Energy loss factor per bounce (default: 0.8)
    - num_bounces: Number of bounces to simulate (default: 4)
    """
    try:
        sim = FreeFallSimulation(
            initial_height=request.initial_height,
            gravity=request.gravity,
            bounce_damping=request.bounce_damping
        )
        return sim.get_trajectory_data(request.num_bounces)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/simulate/free-fall/defaults")
async def free_fall_defaults():
    """Get default parameters for free fall simulation"""
    return {
        "initial_height": 10.0,
        "gravity": 9.81,
        "bounce_damping": 0.8,
        "num_bounces": 4
    }


# Pendulum Endpoints
@app.post("/api/simulate/pendulum", response_model=PendulumResponse)
async def simulate_pendulum(request: PendulumRequest):
    """
    Simulate pendulum motion.
    
    Parameters:
    - length: Pendulum length in meters (default: 1.0)
    - gravity: Acceleration due to gravity (default: 9.81 m/s²)
    - damping: Damping coefficient (default: 0.1)
    - initial_angle: Starting angle in radians (default: π/4 ≈ 0.785)
    - time_duration: Simulation duration in seconds (default: 20.0)
    """
    try:
        sim = PendulumSimulation(
            length=request.length,
            gravity=request.gravity,
            damping=request.damping,
            initial_angle=request.initial_angle
        )
        return sim.get_trajectory_data(request.time_duration)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/simulate/pendulum/defaults")
async def pendulum_defaults():
    """Get default parameters for pendulum simulation"""
    return {
        "length": 1.0,
        "gravity": 9.81,
        "damping": 0.1,
        "initial_angle": 0.785,
        "time_duration": 20.0
    }


# Projectile Endpoints
@app.post("/api/simulate/projectile", response_model=ProjectileResponse)
async def simulate_projectile(request: ProjectileRequest):
    """
    Simulate projectile motion.
    
    Parameters:
    - initial_velocity: Launch velocity in m/s (default: 20.0)
    - launch_angle: Launch angle in degrees (default: 45.0)
    - gravity: Acceleration due to gravity (default: 9.81 m/s²)
    - air_resistance: Air resistance coefficient (default: 0.0)
    - mass: Object mass in kg (default: 1.0)
    """
    try:
        sim = ProjectileSimulation(
            initial_velocity=request.initial_velocity,
            launch_angle=request.launch_angle,
            gravity=request.gravity,
            air_resistance=request.air_resistance,
            mass=request.mass
        )
        return sim.get_trajectory_data()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/simulate/projectile/defaults")
async def projectile_defaults():
    """Get default parameters for projectile simulation"""
    return {
        "initial_velocity": 20.0,
        "launch_angle": 45.0,
        "gravity": 9.81,
        "air_resistance": 0.0,
        "mass": 1.0
    }


# Info Endpoint
@app.get("/api/info")
async def api_info():
    """Get API information and available simulations"""
    return {
        "title": "Physics Simulations API",
        "version": "1.0.0",
        "simulations": [
            {
                "name": "Free Fall",
                "endpoint": "/api/simulate/free-fall",
                "description": "Simulate bouncing ball under gravity"
            },
            {
                "name": "Pendulum",
                "endpoint": "/api/simulate/pendulum",
                "description": "Simulate simple pendulum motion"
            },
            {
                "name": "Projectile",
                "endpoint": "/api/simulate/projectile",
                "description": "Simulate projectile motion with optional air resistance"
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
