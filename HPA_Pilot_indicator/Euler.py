import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from scipy.spatial.transform import Rotation as R

# Euler angles data (pitch, roll, yaw)
euler_angles = [
    [-0.05, 0, -3.12], [-0.05, 0, -3.12], [-0.05, 0, -3.12],
    [-0.05, 0, -3.12], [-0.05, 0, -3.12], [-0.05, 0, -3.12],
    [-0.05, 0, -3.12], [-0.05, 0, -3.12], [-0.05, 0, -3.12],
    [-0.06, 0, -3.12], [-0.06, 0, -3.12], [-0.06, -0.01, -3.12],
    [-0.06, -0.01, -3.12], [-0.06, 0, -3.12], [-0.06, 0.01, -3.12],
    [-0.06, -0.01, -3.12], [-0.06, 0, -3.12], [-0.06, -0.01, -3.12],
    [-0.07, 0, -3.12], [-0.07, -0.01, -3.10], [-0.08, -0.01, -3.11],
    [-0.09, -0.01, -3.10], [-0.09, -0.01, -3.11], [-0.08, 0, -3.12],
    [-0.08, -0.01, -3.13], [-0.09, -0.01, 3.14], [-0.08, -0.01, 3.14],
    [-0.09, -0.01, 3.12], [-0.09, -0.01, 3.08], [-0.08, -0.01, 3.1],
    [-0.09, -0.01, 3.07], [-0.09, -0.02, 3.07], [-0.09, -0.03, 3.1],
    [-0.09, -0.03, 3.11], [-0.09, -0.04, 3.09], [-0.09, -0.05, 3.09],
    [-0.09, -0.06, 3.12], [-0.08, -0.07, 3.12], [-0.07, -0.07, 3.08],
    [-0.09, -0.06, 3.14], [-0.1, -0.05, 3.11], [-0.1, -0.02, 3.13],
    [-0.12, 0, 3.13], [-0.12, -0.01, 3.11], [-0.13, 0.01, -3.13],
    [-0.12, 0.01, 3.11], [-0.12, 0.02, 3.12], [-0.13, 0, 3.13],
    [-0.13, -0.01, 3.13], [-0.14, -0.02, 3.14], [-0.14, -0.02, -3.13],
    [-0.15, -0.02, 3.14], [-0.15, -0.01, -3.14], [-0.16, -0.01, -3.10],
    [-0.15, -0.02, -3.12], [-0.14, -0.03, -3.12], [-0.16, -0.03, -3.10],
    [-0.16, -0.02, -3.07], [-0.17, -0.01, -3.08], [-0.18, 0.01, -3.06],
    [-0.18, 0.02, -3.04], [-0.19, 0, -3.05], [-0.20, 0.01, -3.00],
    [-0.20, 0, -3.02], [-0.21, 0.02, -2.98], [-0.21, -0.03, 3.13],
    [-0.22, -0.04, 3.11], [-0.23, 0.01, -3.14], [-0.23, -0.01, 3.12],
    [-0.25, -0.02, -3.13], [-0.26, -0.03, 3.14], [-0.26, 0, 3.13],
    [-0.27, 0, -3.12], [-0.28, 0, -3.07], [-0.29, 0.01, -3.06],
    [-0.32, 0.03, -3.02], [-0.33, 0.03, -3.02], [-0.31, 0.02, -3.07],
    [-0.27, -0.01, -3.09], [-0.26, -0.06, -3.08], [-0.19, -0.02, 3.05],
    [-0.18, 0.04, -3.13], [-0.19, 0.05, -2.81], [-0.16, 0.07, -2.53]
]


# Function to convert Euler angles to rotation matrix
def euler_to_rotation_matrix(pitch, roll, yaw):
    r = R.from_euler('xyz', [pitch, roll, yaw])
    return r.as_matrix()


# Create figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initialize a 3D plane (simplified as lines representing wings and fuselage)
plane_body, = ax.plot([0, 0], [-1, 1], [0, 0], color="blue")
plane_wings, = ax.plot([-1, 1], [0, 0], [0, 0], color="red")

# Setting the axes properties
ax.set_xlim3d([-2.0, 2.0])
ax.set_ylim3d([-2.0, 2.0])
ax.set_zlim3d([-2.0, 2.0])


# Update function for animation
def update(num):
    # Get Euler angles
    pitch, roll, yaw = euler_angles[num]

    # Get rotation matrix
    rot_matrix = euler_to_rotation_matrix(pitch, roll, yaw)

    # Rotate the plane's body and wings
    body = np.dot(rot_matrix, np.array([[0, 0], [-1, 1], [0, 0]]))
    wings = np.dot(rot_matrix, np.array([[-1, 1], [0, 0], [0, 0]]))

    # Update plane's position in 3D space
    plane_body.set_data(body[0, :], body[1, :])
    plane_body.set_3d_properties(body[2, :])

    plane_wings.set_data(wings[0, :], wings[1, :])
    plane_wings.set_3d_properties(wings[2, :])

# Create animation and store it in
# Create animation and store it in a variable to prevent garbage collection
anim = FuncAnimation(fig, update, frames=len(euler_angles), interval=200)

# Save the animation as a GIF file
anim.save('euler_animation.gif', writer='imagemagick')

# Alternatively, save the animation as an MP4 file
# anim.save('euler_animation.mp4', writer='ffmpeg')

# Show plot (if you also want to see the animation in the console, though it might not work in all environments)
plt.show()
