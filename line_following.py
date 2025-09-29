import pygame
import sys
import os
import math
from classses import robot

class LineFollowingSimulation:
    
    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Line Following robot - Beginner Version")
        
        # Try to load robot image
        robot_img = self.load_robot_img()
        
        # Create robot
        start_pos = (75, 350)  # start in middle-left of screen
        self.robot = robot(start_pos, 100, robot_img)
        
        # Create a simple track
        self.create_track()
        
        # For displaying information
        self.font = pygame.font.Font(None, 16)
        
    def load_robot_img(self):
        
        # List of common robot image filenames to try
        image_files = [
            'robot.png'    ]
        
        for filename in image_files:
            if os.path.exists(filename):
                try:
                    print(f"Loading robot image: {filename}")
                    image = pygame.image.load(filename)
                    return image
                except pygame.error as e:
                    print(f"Could not load {filename}: {e}")
                    continue
        
        print("No robot image found. Using default rectangle shape.")
        return None
    
    def create_track(self):

        
        # Create white background
        self.track = pygame.Surface((self.width, self.height))
        self.track.fill((255, 255, 255))  # white background
        
        # Draw black line
        # You can modify this to create different track shapes
        
        # Option 1: Straight line
        # line_y = 300  # middle of screen
        # pygame.draw.line(self.track, (0, 0, 0), (0, line_y), (self.width, line_y), 20)
        
        for x in range(0, self.width, 2):
            y = 300 + 50 * math.sin(x * 0.01)  # sine wave
            pygame.draw.circle(self.track, (0, 0, 0), (x, int(y)), 10)
        
    def get_sensor_readings(self):
        
        
        sensor_positions = self.robot.get_sensor_positions()
        readings = []
        
        for sensor_x, sensor_y in sensor_positions:
            # Check if sensor is within screen bounds
            if 0 <= sensor_x < self.width and 0 <= sensor_y < self.height:
                # Get pixel color at sensor position
                pixel_color = self.track.get_at((int(sensor_x), int(sensor_y)))
                
                # If pixel is dark (close to black), sensor detects line
                if pixel_color[0] < 100:  # red component < 100 means dark
                    readings.append(1)  # line detected
                else:
                    readings.append(0)  # no line
            else:
                readings.append(0)  # sensor outside screen = no line
        
        return readings
    
    
    
    def draw_info_panel(self, readings):

        robot_info = self.robot.get_info()
        
        # Create semi-transparent background for info panel
        info_panel = pygame.Surface((125, 100))
        info_panel.fill((0, 0, 0))
        info_panel.set_alpha(180)
        self.screen.blit(info_panel, (10, 10))
        
        # Display information
        info_lines = [
            f"Position: {robot_info['position']}",
            f"Heading: {robot_info['heading']:.1f}°",
            f"Sensors: L={readings[0]} C={readings[1]} R={readings[2]}",
            f"Wheels: L={robot_info['wheel_speeds'][0]} R={robot_info['wheel_speeds'][1]}",
            f"Error: {robot_info['last_error']}",
            f"Lost Count: {robot_info['lost_counter']}"
        ]
        
        for i, line in enumerate(info_lines):
            text_surface = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (20, 20 + i * 10))
    
   
    def run(self):

        
        clock = pygame.time.Clock()
        running = True

        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
            
            
            # Get sensor readings
            readings = self.get_sensor_readings()
                
            # Let robot decide what to do
            self.robot.follow_line(readings)
                
            # Move robot
            dt = 0.016  # about 60 FPS
            self.robot.move(dt)
            
            # Draw everything
            self.screen.fill((255, 255, 255))  # white background
            
            # Draw the track
            self.screen.blit(self.track, (0, 0))
            
            # Draw robot
            self.robot.draw(self.screen)
            
            # Draw sensors
            readings = self.get_sensor_readings()
            self.draw_info_panel(readings)
            # Show pause message
            
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Run the simulation
if __name__ == "__main__":
    sim = LineFollowingSimulation()
    sim.run()