from random import choice


class Settings:
    """Class for storing all settings of the game Plant Shooter"""

    def __init__(self):
        """Initializes game settings"""
        # Screen options
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        self.hero_speed = 1.5
        self.hero_limit = 2

        # Bullets options
        self.bullet_speed = 4
        self.bullet_width = 130
        self.bullet_height = 10
        self.bullet_color = (0, 0, 0)
        self.bullets_allowed = 1

        # target options
        self.target_speed = 0.7
        self._num = [-1, 1]
        self.target_direction = choice(self._num)




    def reset_target_speed(self):
        self.target_speed = 0.5
