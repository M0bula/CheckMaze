import pygame
import settings
import random
import time
from menu import Menu
from achievement import Achievement
from maze import generate_maze, save_maze_to_file, load_maze_from_file

class Particle:
    def __init__(self, x, y, color, direction):
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction
        self.size = random.randint(5, 10)
        self.lifetime = random.randint(30, 60)
        self.alpha = 255

    def update(self):
        if self.direction == 'up':
            self.y -= random.uniform(1, 3)
        elif self.direction == 'down':
            self.y += random.uniform(1, 3)
        elif self.direction == 'left':
            self.x -= random.uniform(1, 3)
        elif self.direction == 'right':
            self.x += random.uniform(1, 3)
        self.size = max(1, self.size - 0.1)
        self.alpha = max(0, self.alpha - 5)
        self.lifetime -= 1

    def is_alive(self):
        return self.lifetime > 0 and self.alpha > 0

    def draw(self, screen):
        surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        surface.fill((*self.color, self.alpha))
        pygame.draw.circle(surface, (*self.color, self.alpha), (self.size, self.size), self.size)
        screen.blit(surface, (int(self.x), int(self.y)))

class Game:
    def __init__(self):
        self.player_x = 1
        self.player_y = 1
        self.paused = False
        self.particles = []
        self.gems = {"red": "up", "yellow": "down", "blue": "left", "green": "right"}
        self.chessboard_background = pygame.image.load(settings.CHESSBOARD_IMG).convert()
        self.fence_img = pygame.image.load(settings.FENCE_IMG).convert_alpha()
        self.player_img = pygame.image.load(settings.PLAYER_IMG).convert_alpha()
        self.goal_img = pygame.image.load(settings.GOAL_IMG).convert_alpha()
        self.red_gem = pygame.image.load('images/red_gem.png').convert_alpha()
        self.yellow_gem = pygame.image.load('images/yellow_gem.png').convert_alpha()
        self.blue_gem = pygame.image.load('images/blue_gem.png').convert_alpha()
        self.green_gem = pygame.image.load('images/green_gem.png').convert_alpha()
        gem_size = 100
        self.red_gem = pygame.transform.scale(self.red_gem, (gem_size, gem_size))
        self.yellow_gem = pygame.transform.scale(self.yellow_gem, (gem_size, gem_size))
        self.blue_gem = pygame.transform.scale(self.blue_gem, (gem_size, gem_size))
        self.green_gem = pygame.transform.scale(self.green_gem, (gem_size, gem_size))
        self.chessboard_background = pygame.transform.scale(self.chessboard_background, (settings.EXPANDED_SCREEN_WIDTH // 2 - 150, settings.SCREEN_HEIGHT))
        self.player_img = pygame.transform.scale(self.player_img, (settings.TILE_SIZE, settings.TILE_SIZE))
        self.goal_img = pygame.transform.scale(self.goal_img, (settings.TILE_SIZE, settings.TILE_SIZE))
        self.fence_img = pygame.transform.scale(self.fence_img, (300, settings.SCREEN_HEIGHT))

        self.menu = Menu()
        self.achievement = Achievement()
        
        self.winning_background = pygame.image.load('images/winning_background.png').convert()
        self.losing_background = pygame.image.load('images/losing_background.png').convert()

        self.initialize_game()

        self.gem_positions = {
            "red": (settings.EXPANDED_SCREEN_WIDTH - 250, settings.SCREEN_HEIGHT - 400),
            "yellow": (settings.EXPANDED_SCREEN_WIDTH - 250, settings.SCREEN_HEIGHT - 200),
            "blue": (settings.EXPANDED_SCREEN_WIDTH - 350, settings.SCREEN_HEIGHT - 300),
            "green": (settings.EXPANDED_SCREEN_WIDTH - 150, settings.SCREEN_HEIGHT - 300),
        }

    def load_maze_from_file(self, filepath):
        """Load maze data from a file"""
        maze = []
        with open(filepath, "r") as file:
            for line in file:
                maze.append(list(map(int, line.strip().split())))
        return maze

    def generate_and_save_maze(self, filepath):
        """Generate a new solvable maze and save it to the specified file"""
        maze = generate_maze(width=10, height=10)
        save_maze_to_file(maze, filepath)
        return maze

    def initialize_game(self):
        """Initialize game elements and load a new maze"""
        maze, goal_position = generate_maze(width=10, height=10)
        save_maze_to_file(maze, "maps/level1.txt")
        self.maze = maze
        self.goal_x, self.goal_y = goal_position
        self.player_x, self.player_y = 1, 1
        if self.maze[self.player_y][self.player_x] == 1:
            self.maze[self.player_y][self.player_x] = 0
        self.wall_hit_count = 0
        self.game_active = True

    def reset_game(self):
        """Reset the game to initial state with a new random maze"""
        maze, goal_position = generate_maze(width=10, height=10)
        save_maze_to_file(maze, "maps/level1.txt")
        self.maze = load_maze_from_file("maps/level1.txt")
        self.goal_x, self.goal_y = goal_position
        self.player_x, self.player_y = 1, 1
        if self.maze[self.player_y][self.player_x] == 1:
            self.maze[self.player_y][self.player_x] = 0
        self.wall_hit_count = 0
        self.game_active = True

    def draw_left_view(self, screen):
        screen.blit(self.chessboard_background, (0, 0))
        screen.blit(self.player_img, (self.player_x * settings.TILE_SIZE, self.player_y * settings.TILE_SIZE))
        screen.blit(self.goal_img, (self.goal_x * settings.TILE_SIZE, self.goal_y * settings.TILE_SIZE))



    def draw_right_view(self, screen):
        wall_color = (102, 205, 170)
        path_color = (144, 238, 144)
        white_color = (255, 255, 255)
        particle_colors = [(255, 223, 0), (255, 200, 100), (255, 175, 50)]  # Warm yellow-orange colors for guiding particles

        # Track particles
        if not hasattr(self, 'guiding_particles'):
            self.guiding_particles = []

        current_time = time.time()

        for row in range(len(self.maze)):
            for col in range(len(self.maze[row])):
                if self.maze[row][col] == 0:
                    color = path_color if (row + col) % 2 == 0 else white_color
                else:
                    color = wall_color if (row + col) % 2 == 0 else white_color

                pygame.draw.rect(screen, color, ((settings.EXPANDED_SCREEN_WIDTH // 2) + col * settings.TILE_SIZE, row * settings.TILE_SIZE, settings.TILE_SIZE, settings.TILE_SIZE))

        # Add particles indicating open paths near the player's position
        player_row, player_col = self.player_y, self.player_x
        directions = []
        if player_col < len(self.maze[player_row]) - 1 and self.maze[player_row][player_col + 1] == 0:  # Right is open
            directions.append('right')
        if player_col > 0 and self.maze[player_row][player_col - 1] == 0:  # Left is open
            directions.append('left')
        if player_row > 0 and self.maze[player_row - 1][player_col] == 0:  # Up is open
            directions.append('up')
        if player_row < len(self.maze) - 1 and self.maze[player_row + 1][player_col] == 0:  # Down is open
            directions.append('down')

        for direction in directions:
            # Generate fewer particles for each direction
            for _ in range(2):
                if direction == 'right':
                    vx, vy = random.uniform(0.3, 1.0), random.uniform(-0.5, 0.5)
                elif direction == 'left':
                    vx, vy = random.uniform(-1.0, -0.3), random.uniform(-0.5, 0.5)
                elif direction == 'up':
                    vx, vy = random.uniform(-0.5, 0.5), random.uniform(-1.0, -0.3)
                elif direction == 'down':
                    vx, vy = random.uniform(-0.5, 0.5), random.uniform(0.3, 1.0)

                particle = {
                    'x': (settings.EXPANDED_SCREEN_WIDTH // 2) + self.player_x * settings.TILE_SIZE + random.randint(0, settings.TILE_SIZE),
                    'y': self.player_y * settings.TILE_SIZE + random.randint(0, settings.TILE_SIZE),
                    'vx': vx,
                    'vy': vy,
                    'color': random.choice(particle_colors),
                    'creation_time': current_time,
                    'lifetime': random.uniform(2, 4)  # Lifetime in seconds
                }
                self.guiding_particles.append(particle)

        # Update and draw particles
        for particle in self.guiding_particles[:]:
            # Calculate age of the particle
            age = current_time - particle['creation_time']
            if age > particle['lifetime']:
                self.guiding_particles.remove(particle)
                continue

            # Move particle in its respective direction, floating like in the wind
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']

            # Calculate fading alpha based on age
            alpha = max(0, 255 - int((age / particle['lifetime']) * 255))
            faded_color = (*particle['color'][:3], alpha)

            # Create a surface to draw with alpha transparency
            particle_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, faded_color, (3, 3), 3)
            screen.blit(particle_surface, (int(particle['x']), int(particle['y'])))

        screen.blit(self.player_img, ((settings.EXPANDED_SCREEN_WIDTH // 2) + self.player_x * settings.TILE_SIZE, self.player_y * settings.TILE_SIZE))


        
    def draw_particles(self, screen):
        for particle in self.particles[:]:
            particle.update()
            if particle.is_alive():
                particle.draw(screen)
            else:
                self.particles.remove(particle)

    def draw_game(self, screen):
        self.draw_left_view(screen)
        self.draw_right_view(screen)
        screen.blit(self.fence_img, ((settings.EXPANDED_SCREEN_WIDTH // 2) - 150, 0))
        screen.blit(self.red_gem, self.gem_positions["red"])
        screen.blit(self.yellow_gem, self.gem_positions["yellow"])
        screen.blit(self.blue_gem, self.gem_positions["blue"])
        screen.blit(self.green_gem, self.gem_positions["green"])
        self.draw_particles(screen)

    def check_gem_click(self, mouse_pos):
        for gem, position in self.gem_positions.items():
            rect = pygame.Rect(position[0], position[1], 100, 100)
            if rect.collidepoint(mouse_pos):
                direction = self.gems[gem]
                self.create_particles(direction)
                return direction
        return None

    def create_particles(self, direction):
        color_map = {
            "up": (255, 0, 0),
            "down": (255, 255, 0),
            "left": (0, 0, 255),
            "right": (0, 255, 0),
        }
        color = color_map[direction]
        for _ in range(15):
            particle = Particle(self.player_x * settings.TILE_SIZE + settings.TILE_SIZE // 2,
                                self.player_y * settings.TILE_SIZE + settings.TILE_SIZE // 2,
                                color, direction)
            self.particles.append(particle)

    def update_player(self, direction):
        if direction == 'left' and self.player_x > 0 and self.maze[self.player_y][self.player_x - 1] == 0:
            self.player_x -= 1
        elif direction == 'right' and self.player_x < len(self.maze[0]) - 1 and self.maze[self.player_y][self.player_x + 1] == 0:
            self.player_x += 1
        elif direction == 'up' and self.player_y > 0 and self.maze[self.player_y - 1][self.player_x] == 0:
            self.player_y -= 1
        elif direction == 'down' and self.player_y < len(self.maze) - 1 and self.maze[self.player_y + 1][self.player_x] == 0:
            self.player_y += 1
        else:
            return "wall_hit"
        return "continue"

    def handle_keydown(self, key):
        direction = None
        if key == pygame.K_LEFT or key == pygame.K_a:
            direction = 'left'
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            direction = 'right'
        elif key == pygame.K_UP or key == pygame.K_w:
            direction = 'up'
        elif key == pygame.K_DOWN or key == pygame.K_s:
            direction = 'down'

        if direction:
            state = self.update_player(direction)
            if state == "wall_hit":
                return "wall_hit"
            elif self.player_x == self.goal_x and self.player_y == self.goal_y:
                return "win"
        return "continue"

    def reset_to_main_menu(self, screen):
        # Resize the screen back to the main menu size
        main_menu_width = 800  # Set the desired width for the main menu
        main_menu_height = 600  # Set the desired height for the main menu
        screen = pygame.display.set_mode((main_menu_width, main_menu_height))  # Resize the window

        # Display the main menu after resizing
        self.menu.display_menu(screen)

        
    def show_victory_screen(self, screen):
        # 缩放胜利背景以适应窗口
        scaled_winning_bg = pygame.transform.scale(self.winning_background, (screen.get_width(), screen.get_height()))
        screen.blit(scaled_winning_bg, (0, 0))  # 显示缩放后的胜利背景
        pygame.display.flip()
        pygame.time.wait(5000)  # 显示5秒钟后返回主菜单
        self.reset_to_main_menu(screen)
        self.reset_game()

    def show_loss_screen(self, screen):
        # 缩放失败背景以适应窗口
        scaled_losing_bg = pygame.transform.scale(self.losing_background, (screen.get_width(), screen.get_height()))
        screen.blit(scaled_losing_bg, (0, 0))  # 显示缩放后的失败背景
        pygame.display.flip()
        pygame.time.wait(5000)  # 显示5秒钟后返回主菜单
        self.reset_to_main_menu(screen)
        self.reset_game()
