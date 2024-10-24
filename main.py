import pygame
import sys
import math
import random
import webbrowser
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, EXPANDED_SCREEN_WIDTH
from menu import Menu
from game import Game

pygame.init()

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('CheckMaze ver.1.1')

# Initialize menu and game objects
menu = Menu()
game = Game()

running = True
game_active = False
show_instruction = False  # Whether to display the instruction page
show_info_page = False  # Whether to display the info page

# Load gem images for animation
red_gem = pygame.image.load('images/red_gem.png').convert_alpha()
yellow_gem = pygame.image.load('images/yellow_gem.png').convert_alpha()
blue_gem = pygame.image.load('images/blue_gem.png').convert_alpha()
green_gem = pygame.image.load('images/green_gem.png').convert_alpha()

# Scale gem images
gem_size = 60  # Scale down gems
red_gem = pygame.transform.scale(red_gem, (gem_size, gem_size))
yellow_gem = pygame.transform.scale(yellow_gem, (gem_size, gem_size))
blue_gem = pygame.transform.scale(blue_gem, (gem_size, gem_size))
green_gem = pygame.transform.scale(green_gem, (gem_size, gem_size))

# Particle class
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.color = color
        self.lifetime = random.randint(40, 60)  # Particle lifetime
        self.vx = random.uniform(-1, 1)  # x direction speed
        self.vy = random.uniform(-1, 1)  # y direction speed

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.size = max(1, self.size - 0.1)

    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

# Particle system for gem particle effects
particles = []

def add_particles(x, y, color):
    """Add particles at the given position"""
    for _ in range(5):  # Generate multiple particles
        particles.append(Particle(x, y, color))

def update_particles(screen):
    """Update and draw particles"""
    for particle in particles[:]:
        particle.update()
        if particle.lifetime <= 0:
            particles.remove(particle)
        else:
            particle.draw(screen)

# Load font
try:
    font = pygame.font.Font("fonts/PixelifySans-Regular.ttf", 35)  # Custom font
except:
    font = pygame.font.Font(None, 40)  # Default font if not found

def display_instruction(screen):
    """Display game instruction page with gems orbiting the mouse, creating particle effects"""
    global t
    t += 0.02  # Time increment to control elliptical motion speed

    screen.fill((200, 200, 200))  # Background color

    instruction_text = [
        "Welcome to the CheckMaze!",
        "You: Use the arrow keys",
        "\WASD to move the piece.",
        "Your friend: ",
        "Click on gems",
        "To give directional clues.",
        "It hurts to hit the wall though...",
        "",
        "Press any key to begin..."
    ]

    # Display instruction text
    for i, line in enumerate(instruction_text):
        text_surface = font.render(line, True, (0, 0, 0))
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 150 + i * 50))

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Elliptical motion calculation
    radius_x = 150  # Horizontal radius
    radius_y = 100  # Vertical radius

    # Gems orbiting the mouse
    red_gem_x = mouse_x + radius_x * math.cos(t)
    red_gem_y = mouse_y + radius_y * math.sin(t)
    screen.blit(red_gem, (red_gem_x, red_gem_y))
    add_particles(red_gem_x + gem_size // 2, red_gem_y + gem_size // 2, (255, 0, 0))  # Red gem particles

    yellow_gem_x = mouse_x + radius_x * math.cos(t + math.pi / 2)
    yellow_gem_y = mouse_y + radius_y * math.sin(t + math.pi / 2)
    screen.blit(yellow_gem, (yellow_gem_x, yellow_gem_y))
    add_particles(yellow_gem_x + gem_size // 2, yellow_gem_y + gem_size // 2, (255, 255, 0))  # Yellow gem particles

    blue_gem_x = mouse_x + radius_x * math.cos(t + math.pi)
    blue_gem_y = mouse_y + radius_y * math.sin(t + math.pi)
    screen.blit(blue_gem, (blue_gem_x, blue_gem_y))
    add_particles(blue_gem_x + gem_size // 2, blue_gem_y + gem_size // 2, (0, 0, 255))  # Blue gem particles

    green_gem_x = mouse_x + radius_x * math.cos(t + 3 * math.pi / 2)
    green_gem_y = mouse_y + radius_y * math.sin(t + 3 * math.pi / 2)
    screen.blit(green_gem, (green_gem_x, green_gem_y))
    add_particles(green_gem_x + gem_size // 2, green_gem_y + gem_size // 2, (0, 255, 0))  # Green gem particles

    # Update and draw particle effects
    update_particles(screen)

def display_info_page(screen):
    """Display game info page"""
    screen.fill((100, 100, 100))  # Grey background

    info_text = [
        "CheckMaze",
        "Version: 1.0",
        "Developed by: Mason",
        "Github: github.com/M0bula",
        "You use arrow keys/WASD to move.",
        "Your friend clicks gems",
        "give directional clues.",
        "Collaboration OwO",
        "",
        "Click here to visit his GitHub:",
        "github.com/M0bula"
    ]

    # Display info text
    for i, line in enumerate(info_text):
        text_surface = font.render(line, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 100 + i * 50))
        screen.blit(text_surface, text_rect)

        # Check if it's the GitHub link and store its rect position
        if "M0bula" in line:
            global github_link_rect
            github_link_rect = text_rect

t = 0  # Time variable t for controlling elliptical motion
github_link_rect = None  # Store the position of the GitHub link

# Main loop
while running:
    screen.fill((255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_active and not show_instruction and not show_info_page:
                # Handle menu click
                mouse_pos = pygame.mouse.get_pos()
                action = menu.check_click(mouse_pos)
                if action == 'start':
                    show_instruction = True  # Show instruction page
                elif action == 'quit':
                    pygame.quit()
                    sys.exit()
                elif action == 'info':
                    show_info_page = True  # Show info page
            elif show_info_page:
                # Check if the GitHub link was clicked
                mouse_pos = pygame.mouse.get_pos()
                if github_link_rect and github_link_rect.collidepoint(mouse_pos):
                    webbrowser.open("https://github.com/M0bula")
            elif game_active:
                # Check if gems were clicked
                mouse_pos = pygame.mouse.get_pos()
                direction = game.check_gem_click(mouse_pos)
                if direction:
                    game.create_particles(direction)

        if event.type == pygame.KEYDOWN:
            if show_instruction:
                # Any key press to move from instruction page to game
                show_instruction = False
                game_active = True
                screen = pygame.display.set_mode((EXPANDED_SCREEN_WIDTH, SCREEN_HEIGHT))
            elif show_info_page:
                # Any key press to return from info page to main menu
                show_info_page = False
            elif game_active:
                game_state = game.handle_keydown(event.key)
                if game_state == "win":  # Trigger win condition
                    game.show_victory_screen(screen)
                    game_active = False
                elif game_state == "wall_hit":
                    game.wall_hit_count += 1
                    # Display ouch image
                    ouch_image = pygame.image.load('images/ouch.png').convert_alpha()
                    ouch_rect = ouch_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    screen.fill((255, 255, 255))  # Clear screen before displaying ouch
                    game.draw_game(screen)  # Draw the current game state
                    screen.blit(ouch_image, ouch_rect)
                    pygame.display.flip()
                    pygame.time.wait(500)
                    if game.wall_hit_count >= 10:  # If hit wall 10 times, lose
                        game.show_loss_screen(screen)
                        game_active = False

    if game_active:
        if not game.paused:
            game.draw_game(screen)
    elif show_instruction:
        # Display instruction page
        display_instruction(screen)
    elif show_info_page:
        # Display info page
        display_info_page(screen)
    else:
        # Menu screen
        menu.display_menu(screen)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()