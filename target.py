import pygame
from pygame.sprite import Sprite


class Target(Sprite):

    def __init__(self, ai_game):
        """Initializes the target and assigning the rect attribute"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Loading a target image and assigning the rect attribute
        self.image = pygame.image.load('images/target1.png').convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.midright = self.screen_rect.midright

        # self.rect.x = self.screen.get_rect().width
        # self.rect.y = self.screen.get_rect().height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.top <= 0 or self.rect.bottom >= screen_rect.bottom:
            if self.settings.target_speed <= 5:
                self.settings.target_speed += 0.2
            return True

    def update(self):
        """Crosses the target to the left"""
        self.y -= (self.settings.target_speed * self.settings.target_direction)
        self.rect.y = self.y




