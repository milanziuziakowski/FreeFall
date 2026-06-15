"""
Pendulum Simulation - Wahadło Mathematyczne
Simulates a simple pendulum with optional damping.
Uses elegant Python physics modeling style.
"""

import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class PendulumSimulation:
    def __init__(self, length=1.0, gravity=9.81, damping=0.0, initial_angle=np.pi/4):
        self.L = length
        self.g = gravity
        self.damping = damping
        self.theta0 = initial_angle
        
    def derivs(self, state, t):
        """
        Differential equations for pendulum:
        dθ/dt = ω
        dω/dt = -(g/L)sin(θ) - damping*ω
        """
        theta, omega = state
        dtheta_dt = omega
        domega_dt = -(self.g / self.L) * np.sin(theta) - self.damping * omega
        
        return [dtheta_dt, domega_dt]
    
    def simulate(self, t_max=20.0, dt=0.05):
        """
        Simulate pendulum motion.
        Returns trajectory: list of [angle, angular_velocity] pairs
        """
        t = np.arange(0, t_max, dt)
        state = [self.theta0, 0.0]
        
        trajectory = integrate.odeint(self.derivs, state, t)
        
        return trajectory, dt, t
    
    def get_trajectory_data(self, t_max=20.0):
        """Returns trajectory as dict for API serialization"""
        trajectory, dt, t = self.simulate(t_max)
        
        # Convert polar coordinates to Cartesian for visualization
        x_positions = self.L * np.sin(trajectory[:, 0])
        y_positions = -self.L * np.cos(trajectory[:, 0])
        angles = trajectory[:, 0].tolist()
        
        return {
            "x_positions": x_positions.tolist(),
            "y_positions": y_positions.tolist(),
            "angles": angles,
            "times": t.tolist(),
            "dt": float(dt),
            "length": self.L,
            "gravity": self.g,
            "damping": self.damping,
            "initial_angle": self.theta0
        }


def create_animation(trajectory, length, dt, output_path="wahadlo.htm"):
    """Create and save pendulum animation from trajectory"""
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-length*1.5, length*1.5),
                         ylim=(-length*1.5, length*0.5), frameon=True, picker=None)
    
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    
    # Pivot point
    ax.plot(0, 0, 'ko', markersize=8)
    
    # Pendulum line and bob
    line, = ax.plot([], [], 'o-', lw=2, color='blue', markersize=10)
    time_template = 'time = %.2fs, θ = %.2f rad'
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=10)
    
    def init():
        line.set_data([], [])
        time_text.set_text('')
        return line, time_text
    
    def animate(i):
        theta = trajectory[i, 0]
        x = length * np.sin(theta)
        y = -length * np.cos(theta)
        
        line.set_data([0, x], [0, y])
        time_text.set_text(time_template % (i * dt, theta))
        
        return line, time_text
    
    ani = animation.FuncAnimation(fig, animate, np.arange(len(trajectory)),
                                  interval=25, blit=True, init_func=init)
    ani.save(output_path, fps=20)
    plt.close(fig)


if __name__ == "__main__":
    sim = PendulumSimulation(length=1.0, gravity=9.81, damping=0.1, 
                            initial_angle=np.pi/4)
    trajectory, dt, t = sim.simulate(t_max=20.0)
    create_animation(trajectory, sim.L, dt, "wahadlo.htm")
