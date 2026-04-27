import numpy as np
import matplotlib.pyplot as plt
import csv

file = 'values.csv' # Path to your CSV file

# Read data from CSV file
with open(file, 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

names = [row['name'] for row in rows]
x = [int(row['value']) for row in rows]
rotation_offset = 0  # Rotate all spokes anticlockwise by this angle
rad = [float(row['angle']) + rotation_offset for row in rows]
n = len(names)

# Angles for each bar
width = 2 * np.pi / n

# Adjust widths: half for 'Gender' and 'Self'
widths = [width / 2 if name in ['Gender', 'Self'] else width for name in names]

# Calculate boundary angles for spokes
boundaries = set()
for angle, w in zip(rad, widths):
    # boundaries.add(angle - w / 2)
    # boundaries.add(angle + w / 2)
    boundaries.add(angle + w/2)  # Add the center angle of each spoke as a boundary
boundary_list = sorted(boundaries)

# Suppress radial lines at specific angles
suppress_angles = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi, 5*np.pi/4, 3*np.pi/2, 7*np.pi/4]  # Suppress at these angles (0°, 45°, 90°, etc.)     

# Generate a list of colors from a colormap
colors = plt.cm.tab20(np.linspace(0, 1, n))  # 'tab20' gives 20 distinct colors

plt.figure(figsize=(10, 10))
ax = plt.subplot(polar=True)

# Plot bars with different colors
ax.bar(rad, x, width=widths, color=colors, bottom=0, linewidth=1, edgecolor="black")

# Set radial axis limits and ticks
ax.set_ylim(0, 10)  # Goes out to 10
ax.set_yticks(np.arange(0, 11, 1))  # Keep grid lines
ax.set_yticklabels([])  # Remove numeric labels


# Keep angular ticks for spoke lines
# ax.set_xticks(rad)  # Positions for spoke lines
ax.set_xticklabels([])  # Hide default angular labels

# Draw custom spoke lines with higher alpha, suppressing at specific angles
for angle in boundary_list:
    if not any(np.isclose(angle, s, atol=1e-1) for s in suppress_angles):
        ax.plot([angle , angle], [0, 10], color="black", alpha=0.3, linewidth=1)

# Add multiline to labels by replacing newline `xx` with `\n`
fixed_newline_names = [name.replace("xx", "\n") for name in names]  # Replace newline with space for printing

# Add custom spaced-out labels
label_radius = 11  # Distance from center
for angle, label in zip(rad, fixed_newline_names):
    ax.text(angle, label_radius, label, ha="center", va="center", fontsize=10, multialignment='left')

# Move title further out
ax.set_title("Permission Wheel", fontsize=14, pad=60)  # pad increases distance

# Ensure grid lines are visible
# ax.grid(False)  # Disable grid to avoid overlapping lines

# Add Cartesian axis lines from -10 to 10
# Horizontal axis (y=0)
x_h = np.linspace(-10, 10, 200)
y_h = np.zeros_like(x_h)
r_h = np.sqrt(x_h**2 + y_h**2)
theta_h = np.arctan2(y_h, x_h)
ax.plot(theta_h, r_h, color='black', linewidth=2)

# Vertical axis (x=0)
y_v = np.linspace(-10, 10, 200)
x_v = np.zeros_like(y_v)
r_v = np.sqrt(x_v**2 + y_v**2)
theta_v = np.arctan2(y_v, x_v)
ax.plot(theta_v, r_v, color='black', linewidth=2)

# Add arrows at the ends
ax.annotate('', xy=(0, 10), xytext=(0, 9), arrowprops=dict(arrowstyle='->', color='black', linewidth=2))  # positive x
ax.annotate('', xy=(np.pi, 10), xytext=(np.pi, 9), arrowprops=dict(arrowstyle='->', color='black', linewidth=2))  # negative x
ax.annotate('', xy=(np.pi/2, 10), xytext=(np.pi/2, 9), arrowprops=dict(arrowstyle='->', color='black', linewidth=2))  # positive y
ax.annotate('', xy=(3*np.pi/2, 10), xytext=(3*np.pi/2, 9), arrowprops=dict(arrowstyle='->', color='black', linewidth=2))  # negative y

plt.tight_layout()

# plt.tight_layout()
plt.savefig('permission_wheel.png')
plt.show()
