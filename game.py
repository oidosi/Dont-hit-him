import pygame
from pygame.locals import *
from sys import exit
import os
import random

pygame.init()  # Initialize pygame

screen = pygame.display.set_mode((1600, 800))  # Set up the screen
pygame.display.set_caption('Racing Game')  # Set the window title

clock = pygame.time.Clock()  # Set up the clock

road_surface = pygame.image.load('graphics/Road.png').convert()  # Load road surface image

car_sound = pygame.mixer.Sound(os.path.join('graphics', 'car.wav'))  # Load the sound effect

font = pygame.font.Font(None, 36)  # Set up font for text rendering

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)  # Define blue color for Porsche

start_text = "Press SPACE to start"
instructions = [
   "Instructions:",
   "Control Car: Arrow keys",
   "Control Porsche: W/A/S/D keys",
   "Dodge the Walkers!"
]

def start_screen():
   screen.fill(WHITE)
   start_render = font.render(start_text, True, BLACK)
   screen.blit(start_render, (300, 250))

   for i, instruction in enumerate(instructions):
       instruction_render = font.render(instruction, True, BLACK)
       screen.blit(instruction_render, (300, 300 + i * 40))

   pygame.display.update()

class Car(pygame.sprite.Sprite):
   def __init__(self, image_path, initial_position, speed):
       super().__init__()
       original_image = pygame.image.load(image_path).convert_alpha()
       self.image = pygame.transform.scale(original_image, (int(original_image.get_width() * 0.5), int(original_image.get_height() * 0.5)))
       self.rect = self.image.get_rect(midbottom=initial_position)
       self.speed = speed
       self.alive = True

   def update(self):
       keys = pygame.key.get_pressed()
       if keys[pygame.K_UP]:
           self.rect.y -= self.speed
           car_sound.play()  # Play sound when moving
       elif keys[pygame.K_DOWN]:
           self.rect.y += self.speed
           car_sound.play()  # Play sound when moving
       if keys[pygame.K_LEFT]:
           self.rect.x -= self.speed
           car_sound.play()  # Play sound when moving
       elif keys[pygame.K_RIGHT]:
           self.rect.x += self.speed
           car_sound.play()  # Play sound when moving

       self.handle_collisions()

       # Wrap around screen edges
       if self.rect.left > screen.get_width():
           self.rect.right = 0
       elif self.rect.right < 0:
           self.rect.left = screen.get_width()
       if self.rect.bottom < 0:
           self.rect.top = screen.get_height()
       elif self.rect.top > screen.get_height():
           self.rect.bottom = 0

   def handle_collisions(self):
       for walker in walker_group:
           if self.rect.colliderect(walker.rect):
               self.alive = False
               porsche.alive = True  # Porsche wins if Car hits walker
               break  # Stop checking for collisions after one hit

class Porsche(pygame.sprite.Sprite):
   def __init__(self, image_path, initial_position, speed):
       super().__init__()
       original_image = pygame.image.load(image_path).convert_alpha()
       self.image = pygame.transform.scale(original_image, (int(original_image.get_width() * 0.5), int(original_image.get_height() * 0.5)))
       self.rect = self.image.get_rect(midbottom=initial_position)
       self.speed = speed
       self.alive = True

   def update(self):
       keys = pygame.key.get_pressed()
       if keys[pygame.K_w]:
           self.rect.y -= self.speed
           car_sound.play()  # Play sound when moving
       elif keys[pygame.K_s]:
           self.rect.y += self.speed
           car_sound.play()  # Play sound when moving
       if keys[pygame.K_a]:
           self.rect.x -= self.speed
           car_sound.play()  # Play sound when moving
       elif keys[pygame.K_d]:
           self.rect.x += self.speed
           car_sound.play()  # Play sound when moving

       self.handle_collisions()

       # Wrap around screen edges
       if self.rect.left > screen.get_width():
           self.rect.right = 0
       elif self.rect.right < 0:
           self.rect.left = screen.get_width()
       if self.rect.bottom < 0:
           self.rect.top = screen.get_height()
       elif self.rect.top > screen.get_height():
           self.rect.bottom = 0

   def handle_collisions(self):
       for walker in walker_group:
           if self.rect.colliderect(walker.rect):
               self.alive = False
               car.alive = True  # Car wins if Porsche hits walker
               break  # Stop checking for collisions after one hit

class Walker(pygame.sprite.Sprite):
   def __init__(self, initial_position, speed, direction):
       super().__init__()
       walking_frame_1 = pygame.image.load('graphics/walking.png').convert_alpha()
       walking_frame_2 = pygame.image.load('graphics/walk.png').convert_alpha()
       self.frames = [walking_frame_1, walking_frame_2]
       self.frame_index = 0
       self.image = self.frames[self.frame_index]
       self.rect = self.image.get_rect(midbottom=initial_position)
       self.speed = speed
       self.initial_speed = speed  # Store initial speed
       self.direction = direction  # Direction (1 for horizontal, -1 for vertical)
       self.movement_timer = 0
       self.movement_interval = 1000  # Change movement direction every 1 second

   def update(self):
       self.frame_index += 0.1
       if self.frame_index >= len(self.frames):
           self.frame_index = 0
       self.image = self.frames[int(self.frame_index)]

       # Change movement direction
       self.movement_timer += 1
       if self.movement_timer >= self.movement_interval:
           self.movement_timer = 0
           self.direction *= -1  # Reverse direction

       # Move horizontally or vertically based on direction
       if self.direction == 1:
           self.rect.x += self.speed
       else:
           self.rect.y += self.speed

       # Wrap around screen edges
       if self.rect.right < 0:
           self.rect.left = screen.get_width()
       elif self.rect.left > screen.get_width():
           self.rect.right = 0
       if self.rect.bottom < 0:
           self.rect.top = screen.get_height()
       elif self.rect.top > screen.get_height():
           self.rect.bottom = 0

       # Increase speed after 20 seconds
       if pygame.time.get_ticks() > 20000:
           self.speed = self.initial_speed * (pygame.time.get_ticks() - 20000) / 5000  # Gradually increase speed

# Create instances of the classes and add them to groups
car = Car(os.path.join('graphics', 'car.png'), (300, 200), speed=4)
porsche = Porsche(os.path.join('graphics', 'Porsche.png'), (300, 500), speed=4)

def create_walkers():
   walker1 = Walker((200, screen.get_height()), speed=-2, direction=-1)  # Walker 1 from top
   walker2 = Walker((1400, 0), speed=2, direction=-1)  # Walker 2 from bottom (starts off screen, moving up)
   walker3 = Walker((0, 200), speed=2, direction=1)  # Walker 3 from left (starts off screen, moving right)
   walker4 = Walker((screen.get_width(), 500), speed=-2, direction=1)  # Walker 4 from right (starts off screen, moving left)
   walker_group = pygame.sprite.Group()
   walker_group.add(walker1, walker2, walker3, walker4)
   return walker_group

walker_group = create_walkers()

car_group = pygame.sprite.GroupSingle()
car_group.add(car)

porsche_group = pygame.sprite.GroupSingle()
porsche_group.add(porsche)

# Function to create a new walker
def create_new_walker():
   start_x = random.choice([0, screen.get_width()])
   start_y = random.choice([0, screen.get_height()])
   direction = random.choice([-1, 1])
   speed = -2 * direction
   new_walker = Walker((start_x, start_y), speed, direction)
   walker_group.add(new_walker)

# Main game loop
running = True
show_start_screen = True
game_start_time = 0
speed_up_warning_timer = 0  # Timer for speed up warning message
speed_up_warning_duration = 3000  # Duration of speed up warning message (3 seconds)
winner = None  # To track the winner

while running:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False
       elif event.type == pygame.KEYDOWN:
           if event.key == pygame.K_SPACE and show_start_screen:
               show_start_screen = False
               game_start_time = pygame.time.get_ticks()  # Record game start time
           elif event.key == pygame.K_ESCAPE:
               running = False

   if show_start_screen:
       start_screen()
   else:
       if winner is None:
           if not car.alive:
               winner = "Porsche"
           elif not porsche.alive:
               winner = "Car"

       if winner is not None:
           screen.fill(WHITE)
           winner_text = "Blue Wins!" if winner == "Porsche" else "Red Wins!"
           winner_render = font.render(winner_text, True, BLUE if winner == "Porsche" else RED)
           screen.blit(winner_render, (300, 250))

           pygame.display.update()
       else:
           screen.blit(road_surface, (0, 0))
           car_group.update()
           car_group.draw(screen)
           porsche_group.update()
           porsche_group.draw(screen)
           walker_group.update()
           walker_group.draw(screen)

           # Create a new walker every 5 seconds
           if pygame.time.get_ticks() % 5000 == 0:
               create_new_walker()

           # Display speed up warning message
           if pygame.time.get_ticks() - game_start_time > 15000 and speed_up_warning_timer == 0:
               speed_up_warning_timer = pygame.time.get_ticks()
           if speed_up_warning_timer > 0 and pygame.time.get_ticks() - speed_up_warning_timer < speed_up_warning_duration:
               warning_text = "Speeding Up in 5 Seconds!"
               warning_render = font.render(warning_text, True, YELLOW)
               screen.blit(warning_render, (300, 100))

           # Reset speed up warning timer
           if speed_up_warning_timer > 0 and pygame.time.get_ticks() - speed_up_warning_timer > speed_up_warning_duration:
               speed_up_warning_timer = 0

           pygame.display.update()
           clock.tick(60)  # Cap

pygame.quit()
exit()



