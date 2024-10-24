import pygame
import settings

class Menu:
    def __init__(self):
        # 加载按钮图片
        self.start_button = pygame.image.load(settings.PLAY_BUTTON_IMG).convert_alpha()
        self.quit_button = pygame.image.load(settings.QUIT_BUTTON_IMG).convert_alpha()
        self.info_button = pygame.image.load(settings.INFO_BUTTON_IMG).convert_alpha()
        
        self.start_button = pygame.transform.scale(self.start_button, (220, 80))
        self.quit_button = pygame.transform.scale(self.quit_button, (220, 80))
        self.info_button = pygame.transform.scale(self.info_button, (220, 80))

        self.start_button_rect = self.start_button.get_rect(center=(settings.SCREEN_WIDTH // 2, 600))
        self.quit_button_rect = self.quit_button.get_rect(center=(settings.SCREEN_WIDTH // 2, 680))
        self.info_button_rect = self.info_button.get_rect(center=(settings.SCREEN_WIDTH // 2, 760))

        # 加载主界面背景图片
        self.background = pygame.image.load('images/initial_screen.png').convert()
        self.background = pygame.transform.scale(self.background, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        self.start_button_rect = self.start_button.get_rect(center=(400, 300))  # 屏幕中心左右位置为 400, 上下为 300
        self.quit_button_rect = self.quit_button.get_rect(center=(400, 400))    # 屏幕中心左右位置为 400, 上下为 400
        self.info_button_rect = self.info_button.get_rect(center=(400, 500))    # 屏幕中心左右位置为 400, 上下为 500


    def display_menu(self, screen):
        # 绘制主界面背景
        screen.blit(self.background, (0, 0))
        # 绘制按钮
        screen.blit(self.start_button, self.start_button_rect)
        screen.blit(self.quit_button, self.quit_button_rect)
        screen.blit(self.info_button, self.info_button_rect)

    def check_click(self, mouse_pos):
        if self.start_button_rect.collidepoint(mouse_pos):
            return 'start'
        elif self.quit_button_rect.collidepoint(mouse_pos):
            return 'quit'
        elif self.info_button_rect.collidepoint(mouse_pos):
            return 'info'
        return None
