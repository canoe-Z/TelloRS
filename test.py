from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
import numpy as np
import matplotlib.pyplot as plt
def plot_measurements(xs, ys=None, dt=None, color='k', lw=1, label='Measurements',
                      lines=False, **kwargs):
    """ Helper function to give a consistant way to display
    measurements in the book.
    """
    if ys is None and dt is not None:
        ys = xs
        xs = np.arange(0, len(ys)*dt, dt)

    plt.autoscale(tight=False)
    if lines:
        if ys is not None:
            return plt.plot(xs, ys, color=color, lw=lw, ls='--', label=label, **kwargs)
        else:
            return plt.plot(xs, color=color, lw=lw, ls='--', label=label, **kwargs)
    else:
        if ys is not None:
            return plt.scatter(xs, ys, edgecolor=color, facecolor='none',
                        lw=2, label=label, **kwargs),
        else:
            return plt.scatter(range(len(xs)), xs, edgecolor=color, facecolor='none',
                        lw=2, label=label, **kwargs),

dt = 0.01
R = 1
kf = KalmanFilter(3, 1, 3)
kf.P *= 10
kf.R *= R
kf.Q = np.diag([0.01, 0.01, 0.01])
#kf.Q = Q_discrete_white_noise(3, dt, 0.1)
kf.F = np.diag([1, 1, 1])
kf.F[0, 1] = dt

kf.B = np.array([[0], [dt], [0]])
kf.H = np.array([[0, 1., 1.]])
# dt = 1.
# R = 3.
# kf = KalmanFilter(dim_x=2, dim_z=1, dim_u = 1)
# kf.P *= 10
# kf.R *= R
# kf.Q = Q_discrete_white_noise(2, dt, 0.1)
# kf.F = np.array([[1., 0], [0., 0.]])
# kf.B = np.array([[dt], [ 1.]])
# kf.H = np.array([[1., 0]])

zs = [i + np.random.randn()*R for i in range(1, 100)]
xs = []

print(zs)
cmd_velocity = np.array([1.])
for z in zs:
    kf.predict(u=cmd_velocity)
    kf.update(z)
    xs.append(kf.x[0])

# zs = [i + randn()*R for i in range(1, 100)]
# xs = []
# cmd_velocity = np.array([1.])
# for z in zs:
#     kf.predict(u=cmd_velocity)
#     kf.update(z)
#     xs.append(kf.x[0])

plt.plot(xs, label='Kalman Filter')
plot_measurements(zs)
plt.xlabel('time')
plt.legend(loc=4)
plt.ylabel('distance')
plt.show()

