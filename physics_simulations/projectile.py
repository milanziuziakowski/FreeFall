"""
Projectile Motion Simulation - Ruch Pocisku
Simulates projectile motion with optional air resistance.
Demonstrates elegant Python physics computation.
"""

import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class ProjectileSimulation:
    def __init__(self, initial_velocity=20.0, launch_angle=45, gravity=9.81, 
                 air_resistance=0.0, mass=1.0):
        self.v0 = initial_velocity
        self.angle = np.radians(launch_angle)
        self.g = gravity
        self.air_resistance = air_resistance
        self.mass = mass
        
    def derivs(self, state, t):
        """
        Differential equations for projectile motion:
        dx/dt = vx
        dy/dt = vy
        dvx/dt = -air_resistance * vx
        dvy/dt = -g - air_resistance * vy
        """
        x, y, vx, vy = state
        
        # Air resistance coefficient
        k = self.air_resistance / self.mass if self.mass > 0 else 0
        
        dx_dt = vx
        dy_dt = vy
        dvx_dt = -k * vx
        dvy_dt = -self.g - k * vy
        
        return [dx_dt, dy_dt, dvx_dt, dvy_dt]
    
    def simulate(self, t_max=None):
        """
        Simulate projectile trajectory.
        Returns trajectory: list of [x, y, vx, vy] states
        """
        # Estimate flight time if not provided
        if t_max is None:
            t_max = (2 * self.v0 * np.sin(self.angle)) / self.g + 2
        
        dt = 0.01
        t = np.arange(0, t_max, dt)
        
        vx0 = self.v0 * np.cos(self.angle)
        vy0 = self.v0 * np.sin(self.angle)
        state = [0, 0, vx0, vy0]
        
        trajectory = integrate.odeint(self.derivs, state, t)
        
        # Filter out positions below ground
        trajectory = trajectory[trajectory[:, 1] >= 0]
        
        return trajectory, dt
    
    def get_trajectory_data(self):
        """Returns trajectory as dict for API serialization"""
        trajectory, dt = self.simulate()
        
        x_positions = trajectory[:, 0].tolist()
        y_positions = trajectory[:, 1].tolist()
        vx_positions = trajectory[:, 2].tolist()
        vy_positions = trajectory[:, 3].tolist()
        
        # Calculate range and max height
        max_height = max(y_positions) if y_positions else 0
        range_distance = max(x_positions) if x_positions else 0
        
        return {
            "x_positions": x_positions,
            "y_positions": y_positions,
            "vx_positions": vx_positions,
            "vy_positions": vy_positions,
            "dt": float(dt),
            "initial_velocity": self.v0,
            "launch_angle": np.degrees(self.angle),
            "gravity": self.g,
            "air_resistance": self.air_resistance,
            "max_height": float(max_height),
            "range": float(range_distance)
        }


def create_animation(trajectory, dt, output_path="pocisk.htm"):
    """Create and save projectile animation from trajectory"""
    x_positions = trajectory[:, 0]
    y_positions = trajectory[:, 1]
    
    x_max = max(x_positions) * 1.1
    y_max = max(y_positions) * 1.2
    
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(0, x_max),
                         ylim=(0, y_max), frameon=True)
    
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Height (m)')
    
    # Projectile
    circle = plt.Circle((x_positions[0], y_positions[0]), 0.2, fc='red', alpha=0.7)
    ax.add_patch(circle)
    
    # Trajectory line
    line, = ax.plot([], [], 'b--', lw=1, alpha=0.5)
    
    time_template = 'time = %.2fs, pos = (%.2f, %.2f) m'
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=10)
    
    def init():
        line.set_data([], [])
        time_text.set_text('')
        return line, time_text
    
    def animate(i):
        circle.center = (x_positions[i], y_positions[i])
        
        # Draw trajectory so far
        line.set_data(x_positions[:i+1], y_positions[:i+1])
        
        time_text.set_text(time_template % (i * dt, x_positions[i], y_positions[i]))
        
        return circle, line, time_text
    
    ani = animation.FuncAnimation(fig, animate, np.arange(len(trajectory)),
                                  interval=25, blit=True, init_func=init)
    ani.save(output_path, fps=20)
    plt.close(fig)


if __name__ == "__main__":
    sim = ProjectileSimulation(initial_velocity=20.0, launch_angle=45, 
                              gravity=9.81, air_resistance=0.1)
    trajectory, dt = sim.simulate()
    create_animation(trajectory, dt, "pocisk.htm")
