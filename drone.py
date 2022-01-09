import time
import matplotlib.pyplot as plt
from simple_pid import PID


class drone:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        #self.distance = distance

    def update(self, vx, vy, dt):
        self.x += vx*dt*10
        self.y += vy*dt*10
        #self.distance += v*dt*10
        # Real Model
        time.sleep(0.03)
        return self.x, self.y


if __name__ == '__main__':
    # Write the created model into the main function
    test_drone = drone(0, 0)
    distance = test_drone.x
    # Set three parameters of PID and limit output
    pid = PID(1, 0.01, 0.1, setpoint=500)
    pid.output_limits = (-10, 10)

    # Used to set time parameters
    start_time = time.time()
    last_time = start_time

    # Visualize Output Results
    setpoint, y, x = [], [], []
    vs = []

    # Set System Runtime
    while time.time() - start_time < 10:

        # Setting the time variable dt
        current_time = time.time()
        dt = (current_time - last_time)

        # The variable temp is used as the output in the whole system, and the difference between the variable temp and the ideal value is used as the input in the feedback loop to adjust the change of the variable power.
        v = pid(distance)
        print(distance, v)
        distance, _ = test_drone.update(v, 0, dt)

        # Visualize Output Results
        x += [current_time - start_time]
        y += [distance]
        vs += [v]
        setpoint += [pid.setpoint]
        # Used for initial value assignment of variable temp
        # if current_time - start_time > 0:
        #     pid.setpoint = 0

        last_time = current_time

        # Visualization of Output Results
    plt.plot(x, setpoint, label='target')
    plt.plot(x, y, label='PID')
    plt.plot(x, vs, label='speed')
    plt.xlabel('time')
    plt.ylabel('distance')
    plt.legend()
    plt.show()
