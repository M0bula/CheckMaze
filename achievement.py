# def show_achievement(screen, title, description, achievement_type):
#     # 确保正确加载成就图片
#     if achievement_type == "victory":
#         achievement_bg = pygame.image.load('images/victory_achievement.png').convert_alpha()
#     elif achievement_type == "failure":
#         achievement_bg = pygame.image.load('images/failure_achievement.png').convert_alpha()

#     # 成就背景和文字的位置与绘制
#     bg_rect = achievement_bg.get_rect()
#     bg_rect.bottomright = (screen.get_width() - 20, screen.get_height() - 20)

#     font = pygame.font.Font(None, 36)
#     title_surface = font.render(title, True, (255, 215, 0))
#     description_surface = font.render(description, True, (255, 255, 255))

#     screen.blit(achievement_bg, bg_rect.topleft)
#     screen.blit(title_surface, (bg_rect.x + 20, bg_rect.y + 20))
#     screen.blit(description_surface, (bg_rect.x + 20, bg_rect.y + 60))

#     pygame.display.flip()
#     pygame.time.wait(3000)  # 显示3秒

import pygame

class Achievement:
    def __init__(self):
        # Load the achievement image (icon or badge)
        self.achievement_image = pygame.image.load('images/victory_achievement.png').convert_alpha()

        # Load achievement text
        self.title = "Victory Achieved!"
        self.description = "You have successfully completed the game."

        # Position and timing
        self.display_duration = 3000  # Achievement will display for 3 seconds
        self.start_time = None  # This will store the time when the achievement appears

        # Achievement display position
        self.popup_position = (600, 500)  # Bottom right, adjust this as needed

    def trigger_achievement(self):
        # Start displaying the achievement
        self.start_time = pygame.time.get_ticks()  # Get the current time when the achievement is triggered

    def display_achievement(self, screen):
        if self.start_time:  # Check if the achievement has been triggered
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time < self.display_duration:
                # Display achievement image
                screen.blit(self.achievement_image, self.popup_position)

                # Render the title and description
                font = pygame.font.SysFont(None, 36)
                title_text = font.render(self.title, True, (255, 255, 255))
                description_text = font.render(self.description, True, (255, 255, 255))

                # Display the text near the pop-up
                screen.blit(title_text, (self.popup_position[0] + 10, self.popup_position[1] - 40))
                screen.blit(description_text, (self.popup_position[0] + 10, self.popup_position[1] + 20))
            else:
                # Reset the achievement display after it disappears
                self.start_time = None
