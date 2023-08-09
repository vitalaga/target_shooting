import pygame


class Archer:
    def __init__(self, ai_game):
        """Initializes the hero and sets its selection."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Loads hero image and gets rectangle
        self.image = pygame.image.load('images/archer.png').convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.midleft = self.screen_rect.midleft

        self.y = float(self.rect.y)

        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Updates the player's position based on the flag"""

        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.hero_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.hero_speed

        self.rect.y = self.y

    def blitme(self):
        """Draw player character at current position"""
        self.screen.blit(self.image, self.rect)

    def center_archer(self):
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)
