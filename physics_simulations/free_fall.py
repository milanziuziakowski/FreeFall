"""
Free Fall Simulation - SpadekSwobodny
Simulates a bouncing ball under gravity with energy loss on impact.
Classic physics visualization in elegant Python style.
"""

from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation


class FreeFallSimulation:
    def __init__(self, initial_height=10.0, gravity=9.81, bounce_damping=0.8):
        self.Ho = initial_height
        self.g = gravity
        self.r = self.Ho * 0.01
        self.mi = 17.08 * (10**(-6))
        self.bounce_damping = bounce_damping
        self.t_koncowe = np.sqrt(2 * self.Ho / self.g) + 1
        
    def derivs(self, state, t):
        """Differential equations for free fall: dh/dt = v, dv/dt = -g"""
        dydx = np.zeros_like(state)
        dydx[0] = state[1]
        dydx[1] = -self.g
        return dydx
    
    def simulate(self, num_bounces=4, dt=0.05):
        """
        Simulate ball bounces with energy loss.
        Returns trajectory data: list of [height, velocity] pairs
        """
        t = np.arange(0.05, 10, dt)
        
        # Initial drop
        state = [self.Ho, 0.0]
        y = integrate.odeint(self.derivs, state, t)
        y = [[e, s] for e, s in y if e > 0]
        
        # Subsequent bounces
        for bounce in range(1, num_bounces):
            h_bounce = 0.0
            v_bounce = -self.bounce_damping * y[-1][1]
            
            state = [h_bounce, v_bounce]
            y_bounce = integrate.odeint(self.derivs, state, t)
            y_bounce = [[e, s] for e, s in y_bounce if e > 0]
            
            y = y + y_bounce
        
        return y, dt
    
    def get_trajectory_data(self, num_bounces=4):
        """Returns trajectory as dict for API serialization"""
        y, dt = self.simulate(num_bounces)
        
        x_positions = [0 for _, _ in y]
        y_positions = [e for e, _ in y]
        
        return {
            "x_positions": x_positions,
            "y_positions": y_positions,
            "dt": dt,
            "initial_height": self.Ho,
            "gravity": self.g,
            "radius": self.r,
            "bounce_damping": self.bounce_damping,
            "num_bounces": num_bounces
        }


def create_animation(y, dt, output_path="spadekswobodny.htm"):
    """Create and save animation from trajectory"""
    Ho = max([e for e, _ in y])
    r = Ho * 0.01
    
    fig = plt.figure()
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-0.6*Ho, 0.6*Ho), 
                         ylim=(0, Ho), frameon=False, picker=None)
    
    line, = ax.plot([], [], '', lw=2)
    time_template = 'time = %.1fs'
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
    
    def init():
        line.set_data([], [])
        time_text.set_text('')
        return line, time_text
    
    def animate(i):
        circle = plt.Circle((0, y[i][0]), r, fc='green')
        plt.gca().add_patch(circle)
        time_text.set_text(time_template % (i * dt))
        return circle, time_text
    
    ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y)), 
                                  interval=25, blit=True, init_func=init)
    ani.save(output_path, fps=15)
    plt.close(fig)


if __name__ == "__main__":
    sim = FreeFallSimulation(initial_height=10.0, gravity=9.81, bounce_damping=0.8)
    y, dt = sim.simulate(num_bounces=4)
    create_animation(y, dt, "spadekswobodny.htm")
