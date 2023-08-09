import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class for controlling bullets fired by peas"""

    def __init__(self, ai_game):
        """Creates a bullet object at the player's current position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # self.color = self.settings.bullet_color

        # Creating a bullet at position (0, 0) and assigning the correct position
        # self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.image = pygame.image.load('images/arrow.jpg')
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()

        self.rect.midright = ai_game.archer.rect.midright

        # Bullet position is stored in real format
        self.x = float(self.rect.x)

    def update(self):
        """Moves the bullet to the right on the screen"""
        # Updates bullet positions in real format
        self.x += self.settings.bullet_speed
        # Updates the position of the rectangle
        self.rect.x = self.x

    def draw_bullet(self):
        """Launching a bullet on the screen"""
        self.screen.blit(self.image, self.rect)
