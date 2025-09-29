import numpy as np
import math
import pygame

def distance(pt1, pt2):
    pt1= np.array(pt1)
    pt2= np.array(pt2)
    return np.linalg.norm(pt1-pt2)

class robot:
    def __init__(self, startpos, width, robot_img= None):

        self.m2p= 3779.52 #standard per meter to pixels

        #robot dimensions
        self.w = width
        self.x= startpos[0]
        self.y= startpos[1] 
        self.heading= 0 #robot's orientation in radia

        self.vl= 0.05*self.m2p #meters/sec
        self.vr= 0.05*self.m2p #meters/sec

        self.maxspeed= 0.02*self.m2p #predefined min and max speed
        self.minspeed= 0.01*self.m2p
        
        
        #error tracking for prop control
        self.last_known_error = 0
        self.lost_line_counter = 0
        self.lost_line_thres = 5 
        #no. of cycles before recovery starts
        self.robot= robot_img
        self.robot= pygame.transform.scale(self.robot, (int(self.w), int(self.w)))
        self.original_image = self.robot.copy()
        
    def follow_line(self, readings):
        #readings:- left, right, centre
        #implementing a proportional controller
        wghts= [-1, 0 , 1]
        wghted_sum = 0
        num_act_sens= sum(readings)
        # CASE 1: At least one sensor sees the line
        if num_act_sens> 0:
            # Calculate weighted error
            # If left sensor sees line: error = negative (turn left)
            # If right sensor sees line: error = positive (turn right) 
            # If center sensor sees line: error = 0 (go straight)
            for wght, reading in zip(wghts, readings):
                wghted_sum += wght * reading
            
            error = wghted_sum / num_act_sens
            # Remember this error for later
            self.last_known_error = error

            # Reset lost line counter (we found the line!)
            self.lost_line_counter = 0
            
            # STEP 2: Adjust wheel speeds based on error
            # Basic idea: if error is negative (line on left), slow down left wheel
            #            if error is positive (line on right), slow down right wheel
            
            correction = error * 20  # multiply by 20 to make correction stronger
            
            self.vl = self.minspeed - correction  # left wheel gets faster and right wheel slower so car turns left
            self.vr = self.minspeed + correction  # right wheel, turns right and vice versa


            #speed check
            if self.vl > self.maxspeed:
                self.vl = self.maxspeed
            if self.vl < 0:
                self.vl = 0
                
            if self.vr > self.maxspeed:
                self.vr = self.maxspeed
            if self.vr < 0:
                self.vr = 0
        else: 
            #no sensors detect line
            self.lost_line_counter+=1
            if self.lost_line_counter> self.lost_line_thres:
                #recover by turning and returning to last point
                if self.last_known_error<0:
                    #i.e last error was to left so turn left
                    self.vl=0
                    self.vr= self.minspeed
                elif self.last_known_error > 0:
                    #to right
                    self.vr= 0 
                    self.vl= self.minspeed
                else:
                    #last error was 0 so spin in default direcn
                    self.vl = self.minspeed
                    self.vr= 0
                return
            
            else:
                error= self.last_known_error

    def move(self, dt):

        #dt is elapsed time
        #avg speed of 2 sides
        avg_speed = (self.vl + self.vr) / 2
        
        # Speed difference = how much robot turns
        speed_diff = self.vr - self.vl
        turn_rate = speed_diff / self.w
        
        # Update robot position
        self.x += avg_speed * math.cos(self.heading) * dt
        self.y += avg_speed * math.sin(self.heading) * dt
        self.heading += turn_rate * dt
        
        # Keep heading between -180 and +180 degrees (in radians)
        if self.heading > math.pi:
            self.heading -= 2 * math.pi
        elif self.heading < -math.pi:
            self.heading += 2 * math.pi

    def draw(self, screen):
        
        
        
        # Draw robot image (rotated to match heading)
            
        # Convert heading from radians to degrees
        angle_degrees = math.degrees(self.heading)
            
        # Rotate the image
        rotated_img = pygame.transform.rotate(self.robot, -angle_degrees) #to match the pygame's default anticlockwise, thus -
            
        # Get the rect of the rotated image and center it on robot position
        rect = rotated_img.get_rect()
        rect.center = (int(self.x), int(self.y))
            
        # Draw the rotated image
        screen.blit(rotated_img, rect)
        

    def get_sensor_positions(self):
        
        
        # Sensor positions relative to robot
        sensor_distance = 25  # how far in front of robot
        sensor_spread = 15    # how far apart sensors are
        
        # Calculate sensor positions in world coordinates
        cos_h = math.cos(self.heading)
        sin_h = math.sin(self.heading)
        
        # Left sensor
        left_x = self.x + sensor_distance * cos_h - sensor_spread * sin_h
        left_y = self.y + sensor_distance * sin_h + sensor_spread * cos_h
        
        # Center sensor  
        center_x = self.x + sensor_distance * cos_h
        center_y = self.y + sensor_distance * sin_h
        
        # Right sensor
        right_x = self.x + sensor_distance * cos_h + sensor_spread * sin_h  
        right_y = self.y + sensor_distance * sin_h - sensor_spread * cos_h
        
        return [(left_x, left_y), (center_x, center_y), (right_x, right_y)]

    def get_info(self):
        """Get robot information for display"""
        return {
            'position': (int(self.x), int(self.y)),
            'heading': math.degrees(self.heading),
            'wheel_speeds': (int(self.vl), int(self.vr)),
            'last_error': round(self.last_known_error, 2),
            'lost_counter': self.lost_line_counter
        }