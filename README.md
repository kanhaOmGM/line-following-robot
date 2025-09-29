# line-following-robot
A robot following a line, simulation made in python.

Features
Proportional Line Following: Uses weighted sensor readings to calculate steering corrections
Three-Sensor Array: Left, center, and right sensors detect the line
Recovery Mechanism: Automatically recovers when the line is lost by turning in the direction of the last known error
Visual Representation: Renders a rotatable robot image that accurately reflects heading and position
Real-time Information: Tracks and displays robot state including position, heading, wheel speeds, and error values

Requirements
numpy
pygame


Robot Parameters
Physical Dimensions
Width: Configurable robot width (used for turning calculations)
Meter-to-Pixel Ratio: 3779.52 pixels per meter for accurate simulation scaling
Speed Settings
Base Speed: 0.05 m/s per wheel
Maximum Speed: 0.02 m/s (scaled to pixels)
Minimum Speed: 0.01 m/s (scaled to pixels)
Sensor Configuration
Sensor Distance: 25 pixels in front of robot
Sensor Spread: 15 pixels apart horizontally
Sensor Array: [Left, Center, Right]

Line Following Algorithm
The robot uses a proportional controller with the following logic:

Weighted Error Calculation:
Left sensor: weight = -1 (negative error → turn left)
Center sensor: weight = 0 (zero error → go straight)
Right sensor: weight = +1 (positive error → turn right)
Speed Correction:
   correction = error × 20
   left_wheel_speed = min_speed - correction
   right_wheel_speed = min_speed + correction
Line Loss Recovery:
If no sensors detect the line for more than 5 cycles
Robot turns in the direction of the last known error
Continues until the line is found again
Movement Model



The robot uses differential drive kinematics:

Average Speed: Controls forward motion
Speed Difference: Controls turning rate
Turn Rate: (right_speed - left_speed) / robot_width
Key Methods
follow_line(readings)
Implements the proportional control algorithm. Takes a list of three binary sensor readings [left, center, right] where 1 indicates line detected and 0 indicates no line.

move(dt)
Updates robot position and heading based on wheel speeds and elapsed time using differential drive equations.

draw(screen)
Renders the robot image rotated to match the current heading.

get_sensor_positions()
Returns world coordinates of all three sensors, accounting for robot position and heading.

get_info()
Returns a dictionary containing current robot state for debugging or display purposes.

Usage Example
python
import pygame
from robot import robot

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Load robot image
robot_img = pygame.image.load("robot.png")

# Create robot instance
my_robot = robot(
    startpos=(400, 300),  # Starting position (x, y)
    width=50,              # Robot width in pixels
    robot_img=robot_img    # Robot image
)

# Main simulation loop
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds
    
    # Get sensor readings (example - implement your own line detection)
    sensor_readings = [0, 1, 0]  # [left, center, right]
    
    # Update robot
    my_robot.follow_line(sensor_readings)
    my_robot.move(dt)
    
    # Draw
    screen.fill((255, 255, 255))
    my_robot.draw(screen)
    pygame.display.flip()
    
    # Get debug info
    info = my_robot.get_info()
    print(f"Position: {info['position']}, Heading: {info['heading']:.1f}°")
Control Parameters
Tunable Values
Correction Factor (line 61): Currently set to 20. Increase for more aggressive steering, decrease for smoother turns.
Lost Line Threshold (line 28): Number of cycles before recovery kicks in (default: 5).
Sensor Distance/Spread (lines 135-136): Adjust sensor positioning relative to robot.
Notes
The robot maintains heading in radians internally but provides degrees in the info output
Wheel speeds are automatically clamped between 0 and maximum speed
The coordinate system follows Pygame conventions (0,0 at top-left)
Heading of 0 radians points to the right (positive X direction)
License
This code is provided as-is for educational and simulation purposes.

